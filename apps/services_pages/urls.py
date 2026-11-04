
from django.urls import path

from .routes import SERVICE_ROUTES
from .views import ServicePageView

urlpatterns = [
    path(
        route,
        ServicePageView.as_view(),
        {"slug": slug},
        name=name,
    )
    for slug, (route, name) in SERVICE_ROUTES.items()
]
