from django.urls import path

from .views import CampusAmbassadorView

urlpatterns = [
    # 'campus_ambassador_program' is the name your header, footer and partner pages already use
    path("campus-ambassador/", CampusAmbassadorView.as_view(), name="campus_ambassador_program"),
]