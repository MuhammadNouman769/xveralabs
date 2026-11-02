from django.urls import path

from . import views

urlpatterns = [
    path("partners/", views.PartnersView.as_view(), name="partners"),
    path("partners/investors/", views.InvestorsView.as_view(), name="partners_investors"),
    path("partners/apply/", views.ApplyView.as_view(), name="partner_apply"),
]