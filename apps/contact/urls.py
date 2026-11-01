from django.urls import path

from .views import ChatLeadView, ContactUsView

urlpatterns = [
    path("contact-us/", ContactUsView.as_view(), name="contact_us"),
    path("contact-us/chat/", ChatLeadView.as_view(), name="contact_chat"),
]