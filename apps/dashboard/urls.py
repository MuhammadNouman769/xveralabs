from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="dashboard:login"), name="logout"),
    path("expenses/<int:pk>/receipt/", views.expense_receipt, name="expense_receipt"),
    path("", views.dashboard_home, name="home"),
    path("<slug:key>/export/", views.section_export, name="export"),
    path("<slug:key>/", views.section_list, name="section"),
    path("<slug:key>/new/", views.record_edit, name="create"),
    path("<slug:key>/<int:pk>/", views.record_edit, name="edit"),
    path("<slug:key>/<int:pk>/delete/", views.record_delete, name="delete"),
]
