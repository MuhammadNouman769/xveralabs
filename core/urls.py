from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from .sitemaps import PUBLIC_SITEMAPS
from .seo import robots_txt, sitemap_txt
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": PUBLIC_SITEMAPS}, name="sitemap"),
    path("sitemap.txt", sitemap_txt, name="sitemap_txt"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('about/', include('apps.about_us.urls')),
    path('services/', include('apps.services_pages.urls')),
    path('', include('apps.partners.urls')),
    path('', include('apps.contact.urls')),
    path('careers/', include('apps.careers.urls')),
    path('', include('apps.campus_ambassador.urls')),
]

if settings.DEBUG or settings.SERVE_MEDIA:
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
