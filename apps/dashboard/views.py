import json
import csv
from pathlib import Path
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.expenses.models import Expense
from .registry import SECTIONS, SECTIONS_BY_KEY


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


@_staff_required
def dashboard_home(request):
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
    return render(request, "dashboard/home.html", {"sections": sections})


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
    if key == "expenses":
        today = timezone.localdate()
        expense_summary = {
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
