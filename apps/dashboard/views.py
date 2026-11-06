import json
import csv
import html
from io import BytesIO
from pathlib import Path
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.expenses.models import CompanyIncome, Expense
from .registry import SECTIONS, SECTIONS_BY_KEY


COMPANY_NAME = "Xvera Labs"
COMPANY_WEBSITE_URL = "https://xveralabs.pythonanywhere.com/"
COMPANY_PHONE = "+92 324 8699647"


class DashboardLoginView(auth_views.LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = False

    def form_valid(self, form):
        if not form.get_user().is_active or not form.get_user().is_staff:
            form.add_error(None, "This account does not have dashboard access.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or "/dashboard/"


def _is_staff(user):
    return user.is_authenticated and user.is_active and user.is_staff


def _staff_required(view):
    return user_passes_test(_is_staff, login_url="dashboard:login")(view)


def _section_for_user(request, key):
    section = SECTIONS_BY_KEY.get(key)
    if section is None:
        raise Http404("Dashboard section not found.")
    if section.superuser_only and not request.user.is_superuser:
        raise PermissionDenied
    app_label = section.model._meta.app_label
    model_name = section.model._meta.model_name
    if not request.user.is_superuser and not any(
        request.user.has_perm(f"{app_label}.{action}_{model_name}")
        for action in ("view", "change")
    ):
        raise PermissionDenied
    return section


def _display_value(obj, field_name):
    if field_name == "reference" and hasattr(obj, "reference"):
        value = obj.reference
    elif hasattr(obj, f"get_{field_name}_display"):
        value = getattr(obj, f"get_{field_name}_display")()
    else:
        value = getattr(obj, field_name, "")

    try:
        model_field = obj._meta.get_field(field_name)
    except FieldDoesNotExist:
        model_field = None
    if model_field is not None and model_field.many_to_many:
        value = ", ".join(
            str(item) for item in model_field.value_from_object(obj)
        )
    if field_name == "amount" and isinstance(value, Decimal):
        value = f"{value:,.2f}"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, indent=2)
    return "" if value is None else str(value)


def _record_data(section, record):
    return [
        {"label": field.replace("_", " ").title(), "value": _display_value(record, field)}
        for field in section.detail_fields
    ]


def _column_labels(section):
    return [_column_label(section, field) for field in section.columns]


def _column_label(section, field):
    if field == "reference":
        return "Reference"
    try:
        return str(section.model._meta.get_field(field).verbose_name).title()
    except FieldDoesNotExist:
        return field.replace("_", " ").title()


def _financial_summary():
    income_totals = {
        row["currency"]: row
        for row in CompanyIncome.objects.values("currency").annotate(
            total=Sum("amount"),
            count=Count("pk"),
        )
    }
    received_totals = {
        row["currency"]: row
        for row in CompanyIncome.objects.filter(status=CompanyIncome.Status.RECEIVED)
        .values("currency")
        .annotate(total=Sum("amount"), count=Count("pk"))
    }
    pending_totals = {
        row["currency"]: row
        for row in CompanyIncome.objects.filter(status=CompanyIncome.Status.PENDING)
        .values("currency")
        .annotate(total=Sum("amount"), count=Count("pk"))
    }
    expense_status_totals = {
        (row["currency"], row["status"]): row
        for row in Expense.objects.values("currency", "status")
        .annotate(total=Sum("amount"), count=Count("pk"))
    }
    currencies = (
        set(income_totals)
        | set(received_totals)
        | set(pending_totals)
        | {currency for currency, _status in expense_status_totals}
    )
    if not currencies:
        currencies.add(Expense.Currency.PKR)
    return [
        {
            "currency": currency,
            "income_total": f"{income_totals.get(currency, {}).get('total', Decimal('0')):,.2f}",
            "income_count": income_totals.get(currency, {}).get("count", 0),
            "received": f"{received_totals.get(currency, {}).get('total', Decimal('0')):,.2f}",
            "received_count": received_totals.get(currency, {}).get("count", 0),
            "pending": f"{pending_totals.get(currency, {}).get('total', Decimal('0')):,.2f}",
            "pending_count": pending_totals.get(currency, {}).get("count", 0),
            "expenses": f"{expense_status_totals.get((currency, Expense.Status.PAID), {}).get('total', Decimal('0')):,.2f}",
            "expense_paid_count": expense_status_totals.get((currency, Expense.Status.PAID), {}).get("count", 0),
            "expense_pending": f"{expense_status_totals.get((currency, Expense.Status.PENDING), {}).get('total', Decimal('0')):,.2f}",
            "expense_pending_count": expense_status_totals.get((currency, Expense.Status.PENDING), {}).get("count", 0),
            "expense_total": f"{sum((row['total'] for (item_currency, _status), row in expense_status_totals.items() if item_currency == currency), Decimal('0')):,.2f}",
            "expense_count": sum(row["count"] for (item_currency, _status), row in expense_status_totals.items() if item_currency == currency),
            "balance": f"{received_totals.get(currency, {}).get('total', Decimal('0')) - expense_status_totals.get((currency, Expense.Status.PAID), {}).get('total', Decimal('0')):,.2f}",
        }
        for currency in sorted(currencies)
    ]


def _record_count(amount, count):
    noun = "record" if count == 1 else "records"
    return f"{amount} · {count} {noun}"


def _can_view_finances(user):
    return user.is_superuser or all(
        any(
            user.has_perm(f"expenses.{action}_{model_name}")
            for action in ("view", "change")
        )
        for model_name in ("companyincome", "expense")
    )


@_staff_required
def dashboard_home(request):
    can_view_finances = _can_view_finances(request.user)
    sections = [
        {
            "key": section.key,
            "title": section.title,
            "description": section.description,
            "count": section.model.objects.count(),
            "superuser_only": section.superuser_only,
        }
        for section in SECTIONS
        if (not section.superuser_only or request.user.is_superuser)
        and (
            request.user.is_superuser
            or any(
                request.user.has_perm(
                    f"{section.model._meta.app_label}.{action}_{section.model._meta.model_name}"
                )
                for action in ("view", "change")
            )
        )
    ]
    return render(
        request,
        "dashboard/home.html",
        {
            "sections": sections,
            "can_view_finances": can_view_finances,
            "financial_summary": _financial_summary() if can_view_finances else None,
        },
    )


@_staff_required
def section_list(request, key):
    section = _section_for_user(request, key)
    queryset = section.model.objects.all()
    if not section.model._meta.ordering:
        queryset = queryset.order_by("pk")
    search = request.GET.get("q", "").strip()
    if search and section.search_fields:
        condition = Q()
        for field in section.search_fields:
            condition |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(condition)
    expense_summary = None
    financial_summary = None
    can_view_finances = _can_view_finances(request.user)
    if key == "expenses":
        today = timezone.localdate()
        expense_totals_by_currency = {}
        for item in (
            Expense.objects.values("currency", "status")
            .annotate(total=Sum("amount"), count=Count("pk"))
            .order_by("currency", "status")
        ):
            currency_summary = expense_totals_by_currency.setdefault(
                item["currency"],
                {
                    "total": Decimal("0"),
                    "paid": Decimal("0"),
                    "pending": Decimal("0"),
                    "paid_count": 0,
                    "pending_count": 0,
                },
            )
            currency_summary["total"] += item["total"]
            if item["status"] == Expense.Status.PAID:
                currency_summary["paid"] = item["total"]
                currency_summary["paid_count"] = item["count"]
            elif item["status"] == Expense.Status.PENDING:
                currency_summary["pending"] = item["total"]
                currency_summary["pending_count"] = item["count"]

        expense_summary = {
            "payment_totals": [
                {
                    "currency": currency,
                    "total": f'{totals["total"]:,.2f}',
                    "paid": f'{totals["paid"]:,.2f}',
                    "paid_count": totals["paid_count"],
                    "pending": f'{totals["pending"]:,.2f}',
                    "pending_count": totals["pending_count"],
                }
                for currency, totals in sorted(expense_totals_by_currency.items())
            ],
            "monthly_totals": [
                {
                    "currency": item["currency"],
                    "total": f'{item["total"]:,.2f}',
                }
                for item in Expense.objects.filter(
                expense_date__year=today.year,
                expense_date__month=today.month,
            )
            .values("currency")
            .annotate(total=Sum("amount"))
            .order_by("currency")
            ],
            "pending_count": Expense.objects.filter(status=Expense.Status.PENDING).count(),
        }
    elif key == "income" and can_view_finances:
        financial_summary = _financial_summary()

    paginator = Paginator(queryset, 25)
    page_obj = paginator.get_page(request.GET.get("page"))
    rows = [
        {
            "record": record,
            "values": [_display_value(record, field) for field in section.columns],
        }
        for record in page_obj.object_list
    ]
    return render(
        request,
        "dashboard/list.html",
        {
            "section": section,
            "page_obj": page_obj,
            "rows": rows,
            "search": search,
            "column_labels": _column_labels(section),
            "active_section": section.key,
            "can_add": request.user.is_superuser or request.user.has_perm(
                f"{section.model._meta.app_label}.add_{section.model._meta.model_name}"
            ),
            "expense_summary": expense_summary,
            "financial_summary": financial_summary,
            "can_view_finances": can_view_finances,
        },
    )


@_staff_required
def record_edit(request, key, pk=None):
    section = _section_for_user(request, key)
    can_change = request.user.is_superuser or request.user.has_perm(
        f"{section.model._meta.app_label}.change_{section.model._meta.model_name}"
    )
    if pk is None and not request.user.is_superuser and not request.user.has_perm(
        f"{section.model._meta.app_label}.add_{section.model._meta.model_name}"
    ):
        raise PermissionDenied
    if pk is not None and request.method == "POST" and not can_change:
        raise PermissionDenied
    if pk is None and not section.addable:
        raise Http404("New records cannot be created in this section.")
    record = get_object_or_404(section.model, pk=pk) if pk is not None else None
    form_class = section.form_class or modelform_factory(
        section.model,
        fields=section.fields,
    )
    can_view_finances = (
        key in ("income", "expenses") and _can_view_finances(request.user)
    )
    financial_summary = _financial_summary() if can_view_finances else None

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=record)
        if form.is_valid():
            if (
                key == "users"
                and record is not None
                and record.pk == request.user.pk
                and not (
                    form.cleaned_data["is_active"]
                    and form.cleaned_data["is_staff"]
                    and form.cleaned_data["is_superuser"]
                )
            ):
                form.add_error(None, "You cannot remove your own administrator access.")
                return render(
                    request,
                    "dashboard/form.html",
                    {
                        "section": section,
                        "form": form,
                        "record": record,
                        "record_data": _record_data(section, record),
                        "active_section": section.key,
                        "can_change": can_change,
                        "can_delete": request.user.is_superuser or request.user.has_perm(
                            f"{section.model._meta.app_label}.delete_{section.model._meta.model_name}"
                        ),
                        "financial_summary": financial_summary,
                        "can_view_finances": can_view_finances,
                    },
                )
            saved = form.save(commit=False)
            if record is None and section.recorded_by_field:
                setattr(saved, section.recorded_by_field, request.user)
            saved.save()
            form.save_m2m()
            messages.success(request, "Record saved.")
            return redirect("dashboard:edit", key=section.key, pk=saved.pk)
    else:
        form = form_class(instance=record)

    if not can_change and record is not None:
        for field in form.fields.values():
            field.disabled = True

    return render(
        request,
        "dashboard/form.html",
        {
            "section": section,
            "form": form,
            "record": record,
            "record_data": _record_data(section, record) if record else [],
            "active_section": section.key,
            "can_change": can_change,
            "can_delete": request.user.is_superuser or request.user.has_perm(
                f"{section.model._meta.app_label}.delete_{section.model._meta.model_name}"
            ),
            "financial_summary": financial_summary,
            "can_view_finances": can_view_finances,
        },
    )


@_staff_required
def record_delete(request, key, pk):
    section = _section_for_user(request, key)
    if not request.user.is_superuser and not request.user.has_perm(
        f"{section.model._meta.app_label}.delete_{section.model._meta.model_name}"
    ):
        raise PermissionDenied
    record = get_object_or_404(section.model, pk=pk)
    if not section.deletable:
        raise Http404("Records in this section cannot be deleted here.")
    if key == "users" and record.pk == request.user.pk:
        raise PermissionDenied("You cannot delete your own account.")
    if request.method == "POST":
        record.delete()
        messages.success(request, f"Record removed from {section.title}.")
        return redirect("dashboard:section", key=section.key)
    return render(
        request,
        "dashboard/delete.html",
        {"section": section, "record": record, "active_section": section.key},
    )


@_staff_required
def section_export(request, key):
    section = _section_for_user(request, key)
    if not section.export_fields:
        raise Http404("Export is not available for this section.")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{section.key}.csv"'
    writer = csv.writer(response)
    writer.writerow(_column_label(section, field) for field in section.export_fields)
    for record in section.model.objects.all().iterator():
        writer.writerow(
            _spreadsheet_safe(_display_value(record, field))
            for field in section.export_fields
        )
    return response


@_staff_required
def financial_report(request):
    _section_for_user(request, "income")
    _section_for_user(request, "expenses")

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportHeading", parent=styles["Heading2"], fontSize=12, leading=15, spaceBefore=8))
    story = [
        _pdf_brand_header(
            styles,
            "Company Financial Report",
            timezone.localtime().strftime("%Y-%m-%d %H:%M %Z"),
            landscape(A4)[0] - 30 * mm,
        ),
        Spacer(1, 6 * mm),
        Paragraph("Financial summary (amounts remain grouped by currency)", styles["ReportHeading"]),
    ]
    summary_rows = [[
        "Currency", "Total income (amount · records)", "Received (amount · records)",
        "Outstanding income (amount · records)", "Paid expenses (amount · records)",
        "Available balance",
    ]]
    summary_rows.extend([
        [
            item["currency"],
            _record_count(item["income_total"], item["income_count"]),
            _record_count(item["received"], item["received_count"]),
            _record_count(item["pending"], item["pending_count"]),
            _record_count(item["expenses"], item["expense_paid_count"]),
            item["balance"],
        ]
        for item in _financial_summary()
    ] or [["—", "0.00", "0.00", "0.00", "0.00", "0.00"]])
    story.append(_report_table(summary_rows, [30, 50, 48, 52, 48, 39]))

    income_rows = [["Date", "Source", "Income", "Payer", "Amount", "Currency", "Status", "Reference"]]
    income_rows.extend([
        [
            item.income_date.isoformat(),
            item.source,
            item.title,
            item.payer,
            f"{item.amount:,.2f}",
            item.currency,
            item.get_status_display(),
            item.reference,
        ]
        for item in CompanyIncome.objects.all()
    ] or [["—", "No income entries", "", "", "", "", "", ""]])
    story.extend([
        Paragraph("Income entries", styles["ReportHeading"]),
        _report_table(income_rows, [24, 42, 52, 40, 30, 22, 32, 25]),
    ])

    expense_rows = [[
        "Date", "Reference", "Expense", "Category", "Vendor", "Amount", "Currency", "Status",
    ]]
    expense_rows.extend([
        [
            item.expense_date.isoformat(),
            item.reference,
            item.title,
            item.get_category_display(),
            item.vendor,
            f"{item.amount:,.2f}",
            item.currency,
            item.get_status_display(),
        ]
        for item in Expense.objects.all()
    ] or [["—", "—", "No expense entries", "", "", "", "", ""]])
    story.extend([
        Paragraph("Expense entries", styles["ReportHeading"]),
        _report_table(expense_rows, [22, 28, 44, 40, 38, 30, 20, 36]),
    ])
    story.extend([
        Spacer(1, 18 * mm),
        _pdf_signature_block(styles, landscape(A4)[0] - 30 * mm),
    ])
    document.build(story)
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"company-financial-report-{timezone.localdate().isoformat()}.pdf",
        content_type="application/pdf",
    )


@_staff_required
def financial_record_pdf(request, key, pk):
    section = _section_for_user(request, key)
    if key not in ("income", "expenses"):
        raise Http404("Financial record PDF is not available.")
    record = get_object_or_404(section.model, pk=pk)
    if key == "income":
        fields = (
            "reference", "income_date", "title", "source", "payer", "amount",
            "currency", "payment_method", "status", "notes",
        )
        report_title = "Company income record"
        filename = f"income-{record.pk}.pdf"
    else:
        fields = (
            "reference", "expense_date", "title", "category", "vendor", "amount",
            "currency", "payment_method", "status", "notes",
        )
        report_title = "Company expense record"
        filename = f"expense-{record.pk}.pdf"

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    generated_at = timezone.localtime().strftime("%Y-%m-%d %H:%M %Z")
    story = [
        _pdf_brand_header(
            styles,
            report_title,
            f"{generated_at}<br/>Reference: {html.escape(record.reference)}",
            A4[0] - 40 * mm,
        ),
        Spacer(1, 8 * mm),
    ]
    rows = [["Field", "Details"]]
    rows.extend([
        [_column_label(section, field), _display_value(record, field) or "—"]
        for field in fields
    ])
    story.append(_report_table(rows, [45, 130]))
    story.extend([
        Spacer(1, 25 * mm),
        _pdf_signature_block(styles, A4[0] - 40 * mm),
    ])
    document.build(story)
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )


def _pdf_brand_header(styles, title, detail, available_width):
    company_style = ParagraphStyle(
        name="PdfCompanyBrand",
        parent=styles["BodyText"],
        leading=14,
    )
    report_style = ParagraphStyle(
        name="PdfReportTitle",
        parent=styles["Heading2"],
        alignment=2,
        leading=14,
    )
    company = Paragraph(
        f'<font size="15"><b>{html.escape(COMPANY_NAME)}</b></font><br/>'
        f'<link href="{html.escape(COMPANY_WEBSITE_URL, quote=True)}">'
        f'{html.escape(COMPANY_WEBSITE_URL)}</link><br/>'
        f'{html.escape(COMPANY_PHONE)}',
        company_style,
    )
    report = Paragraph(
        f"<b>{html.escape(title)}</b><br/>{detail}",
        report_style,
    )
    table = Table(
        [[company, report]],
        colWidths=[available_width * 0.58, available_width * 0.42],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#087c72")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def _pdf_signature_block(styles, available_width):
    signature_style = ParagraphStyle(
        name="PdfSignatureLabel",
        parent=styles["BodyText"],
        fontSize=9,
        alignment=TA_LEFT,
    )
    signature_line_style = ParagraphStyle(
        name="PdfSignatureLine",
        parent=signature_style,
        alignment=TA_LEFT,
    )
    table = Table(
        [[
            Paragraph("________________________________", signature_line_style),
            Paragraph("________________________________", signature_line_style),
        ], [
            Paragraph("Authorized Signature", signature_style),
            Paragraph("Received / Acknowledged By", signature_style),
        ]],
        colWidths=[available_width / 2, available_width / 2],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def _report_table(rows, widths_mm):
    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        name="FinancialReportCell",
        parent=styles["BodyText"],
        fontSize=7,
        leading=9,
        alignment=TA_LEFT,
    )
    header_style = ParagraphStyle(
        name="FinancialReportHeader",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    formatted_rows = [
        [
            Paragraph(html.escape(str(value)) or "-", header_style if row_index == 0 else cell_style)
            for value in row
        ]
        for row_index, row in enumerate(rows)
    ]
    table = Table(
        formatted_rows,
        colWidths=[width * mm for width in widths_mm],
        repeatRows=1,
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183b36")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#dce6e3")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f8f7")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


@_staff_required
def expense_receipt(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if not request.user.is_superuser and not any(
        request.user.has_perm(f"expenses.{action}_expense")
        for action in ("view", "change")
    ):
        raise PermissionDenied
    if not expense.receipt:
        raise Http404("This expense does not have a receipt.")
    return FileResponse(
        expense.receipt.open("rb"),
        as_attachment=True,
        filename=Path(expense.receipt.name).name,
    )


def _spreadsheet_safe(value):
    if value.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")):
        return f"'{value}"
    return value
