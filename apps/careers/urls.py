from django.urls import path

from . import views

urlpatterns = [
    # both names point to the list page: 'careeers' is the name your header/footer already use
    path("careers/", views.CareersView.as_view(), name="careeers"),
    path("careers/", views.CareersView.as_view(), name="careers"),
    path("careers/apply/", views.GeneralApplyView.as_view(), name="career_apply"),
    path("careers/cv/<int:pk>/", views.cv_download, name="career_cv"),
    path("careers/<slug:slug>/", views.PositionView.as_view(), name="career_detail"),
]