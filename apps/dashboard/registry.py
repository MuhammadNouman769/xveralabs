from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.about_us.models import Team
from apps.blogs.models import Resource
from apps.campus_ambassador.models import Application as AmbassadorApplication
from apps.campus_ambassador.models import Cohort, ProgramItem, Story
from apps.careers.models import JobApplication, JobPosition
from apps.contact.models import ContactMessage
from apps.dashboard.forms import GroupForm, StaffUserForm
from apps.expenses.forms import CompanyIncomeForm, ExpenseForm
from apps.expenses.models import CompanyIncome, Expense
from apps.main.models import IndustryCaseStudy, IndustryCaseStudyBlock
from apps.partners.models import PartnerApplication
from apps.services_pages.models import ServiceBlock, ServiceGroup, ServicePage


@dataclass(frozen=True)
class Section:
    key: str
    title: str
    description: str
    model: type
    fields: tuple[str, ...]
    columns: tuple[str, ...]
    search_fields: tuple[str, ...]
    detail_fields: tuple[str, ...]
    addable: bool = True
    deletable: bool = True
    superuser_only: bool = False
    form_class: type | None = None
    export_fields: tuple[str, ...] = ()
    recorded_by_field: str | None = None


SECTIONS = (
    Section("services", "Service pages", "Edit the published service pages and their SEO content.", ServicePage,
            ("group", "title", "short_title", "slug", "tagline", "meta_description", "intro", "order", "is_published", "is_active"),
            ("title", "group", "is_published", "updated_at"), ("title", "tagline", "intro"),
            ("group", "title", "short_title", "slug", "tagline", "meta_description", "intro", "order", "is_published", "is_active", "created_at", "updated_at")),
    Section("service-groups", "Service groups", "Organize service pages into navigation groups.", ServiceGroup,
            ("name", "slug", "order", "is_active"), ("name", "slug", "order", "is_active"),
            ("name", "slug"), ("name", "slug", "order", "is_active", "created_at", "updated_at")),
    Section("service-blocks", "Service content blocks", "Manage service page features, FAQs, steps, and long-form sections.", ServiceBlock,
            ("page", "kind", "title", "text", "order", "is_active"), ("title", "page", "kind", "order", "is_active"),
            ("title", "text", "page__title"), ("page", "kind", "title", "text", "order", "is_active")),
    Section("industries", "Industry case studies", "Manage industry landing pages and their publishing status.", IndustryCaseStudy,
            ("name", "slug", "eyebrow", "title", "summary", "image_url", "image_alt", "challenge", "approach", "order", "is_published", "is_active"),
            ("name", "title", "is_published", "order"), ("name", "title", "summary", "challenge", "approach"),
            ("name", "slug", "eyebrow", "title", "summary", "image_url", "image_alt", "challenge", "approach", "order", "is_published", "is_active", "created_at", "updated_at")),
    Section("industry-blocks", "Industry content blocks", "Edit capability and consideration blocks for industries.", IndustryCaseStudyBlock,
            ("case_study", "kind", "title", "text", "order", "is_active"), ("title", "case_study", "kind", "order", "is_active"),
            ("title", "text", "case_study__name"), ("case_study", "kind", "title", "text", "order", "is_active")),
    Section("resources", "Resources", "Create and edit articles, guides, reports, and their structured content.", Resource,
            ("title", "slug", "category", "topic", "kind", "read_time", "excerpt", "image", "image_alt", "sections", "order", "is_published"),
            ("title", "category", "kind", "topic", "is_published", "order"), ("title", "category", "excerpt"),
            ("title", "slug", "category", "topic", "kind", "read_time", "excerpt", "image", "image_alt", "sections", "order", "is_published", "created_at", "updated_at")),
    Section("expenses", "Company expenses", "Record company spending, receipts, and payment status.", Expense,
            ("title", "category", "expense_date", "vendor", "amount", "currency", "payment_method", "status"),
            ("expense_date", "title", "category", "vendor", "amount", "currency", "status"),
            ("title", "vendor", "reference", "notes"),
            ("title", "category", "expense_date", "vendor", "amount", "currency", "payment_method", "status", "reference", "notes", "receipt", "recorded_by", "created_at", "updated_at"),
            form_class=ExpenseForm, export_fields=("expense_date", "title", "category", "vendor", "amount", "currency", "payment_method", "status", "reference", "recorded_by", "notes"), recorded_by_field="recorded_by"),
    Section("income", "Company income", "Track where company income comes from, what has been received, and what is pending.", CompanyIncome,
            ("title", "source", "income_date", "payer", "amount", "currency", "payment_method", "status"),
            ("income_date", "source", "title", "payer", "amount", "currency", "status"),
            ("title", "source", "payer", "reference", "notes"),
            ("title", "source", "income_date", "payer", "amount", "currency", "payment_method", "status", "reference", "notes", "recorded_by", "created_at", "updated_at"),
            form_class=CompanyIncomeForm, export_fields=("income_date", "source", "title", "payer", "amount", "currency", "payment_method", "status", "reference", "recorded_by", "notes"), recorded_by_field="recorded_by"),
    Section("contacts", "Contact messages", "Review incoming project and partnership enquiries.", ContactMessage,
            ("status",), ("created_at", "full_name", "company", "topic", "region", "status"),
            ("full_name", "email", "company", "phone", "details"),
            ("created_at", "full_name", "email", "phone", "company", "company_url", "topic", "region", "services", "details", "budget", "source", "page_url", "status"),
            addable=False),
    Section("jobs", "Career positions", "Publish, update, and close job listings and internships.", JobPosition,
            ("title", "slug", "department", "job_type", "work_mode", "level", "location", "duration", "compensation", "summary", "description", "responsibilities", "requirements", "nice_to_have", "is_open", "is_featured", "deadline", "is_active"),
            ("title", "department", "job_type", "is_open", "is_featured", "deadline"),
            ("title", "summary", "description"),
            ("title", "slug", "department", "job_type", "work_mode", "level", "location", "duration", "compensation", "summary", "description", "responsibilities", "requirements", "nice_to_have", "is_open", "is_featured", "deadline", "is_active", "created_at", "updated_at")),
    Section("job-applications", "Career applications", "Review applicant details and update internal status and notes.", JobApplication,
            ("status", "internal_notes"), ("created_at", "reference", "full_name", "position_title", "email", "status"),
            ("full_name", "email", "phone", "position_title", "cover_note"),
            ("reference", "created_at", "full_name", "email", "phone", "city", "profile_url", "position_title", "cover_note", "consent", "status", "internal_notes"),
            addable=False, export_fields=("created_at", "reference", "position_title", "full_name", "email", "phone", "city", "profile_url", "status", "cover_note")),
    Section("team", "Team", "Manage team profiles shown on the public website.", Team,
            ("first_name", "last_name", "designation", "linkedin_link", "image", "display_order", "is_active"),
            ("first_name", "last_name", "designation", "display_order", "is_active"),
            ("first_name", "last_name", "designation"), ("first_name", "last_name", "designation", "linkedin_link", "image", "display_order", "is_active", "created_at", "updated_at")),
    Section("partner-applications", "Partner applications", "Review partner and investor applications.", PartnerApplication,
            ("status", "internal_notes"), ("created_at", "reference", "full_name", "partner_type", "company", "region", "status"),
            ("full_name", "email", "company", "phone", "message"),
            ("created_at", "reference", "partner_type", "full_name", "email", "phone_code", "phone", "company", "region", "module", "investment_range", "heard_from", "message", "consent", "status", "internal_notes"),
            addable=False, export_fields=("created_at", "reference", "partner_type", "full_name", "email", "phone", "company", "region", "module", "investment_range", "status", "message")),
    Section("ambassador-cohorts", "Ambassador cohorts", "Manage application windows and cohort details.", Cohort,
            ("name", "is_open", "opens_on", "closes_on", "term_months", "hours_per_week", "eligibility", "is_active"),
            ("name", "is_open", "opens_on", "closes_on", "is_active"), ("name", "eligibility"),
            ("name", "is_open", "opens_on", "closes_on", "term_months", "hours_per_week", "eligibility", "is_active", "created_at", "updated_at")),
    Section("ambassador-content", "Ambassador page content", "Manage benefits, steps, responsibilities, and FAQs.", ProgramItem,
            ("kind", "title", "text", "order", "is_active"), ("title", "kind", "order", "is_active"),
            ("title", "text"), ("kind", "title", "text", "order", "is_active")),
    Section("ambassador-stories", "Ambassador stories", "Manage published ambassador testimonials.", Story,
            ("name", "university", "label", "quote", "is_published", "order", "is_active"),
            ("name", "university", "is_published", "order"), ("name", "university", "quote"),
            ("name", "university", "label", "quote", "is_published", "order", "is_active", "created_at", "updated_at")),
    Section("ambassador-applications", "Ambassador applications", "Review student applications and manage their status.", AmbassadorApplication,
            ("status", "internal_notes"), ("created_at", "full_name", "university", "city", "year_of_study", "status"),
            ("full_name", "email", "phone", "university", "city", "motivation"),
            ("created_at", "full_name", "email", "phone", "university", "city", "degree", "year_of_study", "social_url", "motivation", "experience", "is_student", "consent", "status", "internal_notes"),
            addable=False, export_fields=("created_at", "reference", "full_name", "email", "phone", "university", "city", "degree", "year_of_study", "social_url", "status", "motivation")),
    Section("users", "Staff accounts", "Control site staff access. Only superusers can open this section.", get_user_model(),
            ("username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser", "groups", "user_permissions", "password"),
            ("username", "email", "is_active", "is_staff", "is_superuser"), ("username", "email", "first_name", "last_name"),
            ("username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser", "groups"),
            superuser_only=True, form_class=StaffUserForm),
    Section("groups", "Permission groups", "Assign Django permissions to staff groups. Only superusers can open this section.", Group,
            ("name", "permissions"), ("name",), ("name",), ("name", "permissions"),
            superuser_only=True, form_class=GroupForm),
)

SECTIONS_BY_KEY = {section.key: section for section in SECTIONS}
