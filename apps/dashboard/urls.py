from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="dashboard:login"), name="logout"),
    path("income/<int:pk>/pdf/", views.financial_record_pdf, {"key": "income"}, name="income_pdf"),
    path("expenses/<int:pk>/receipt/", views.expense_receipt, name="expense_receipt"),
    path("expenses/<int:pk>/pdf/", views.financial_record_pdf, {"key": "expenses"}, name="expense_pdf"),
    path("financial-report.pdf", views.financial_report, name="financial_report"),
    path("", views.dashboard_home, name="home"),
    path("<slug:key>/export/", views.section_export, name="export"),
    path("<slug:key>/", views.section_list, name="section"),
    path("<slug:key>/new/", views.record_edit, name="create"),
    path("<slug:key>/<int:pk>/", views.record_edit, name="edit"),
    path("<slug:key>/<int:pk>/delete/", views.record_delete, name="delete"),
]
