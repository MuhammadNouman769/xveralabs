from django.http import HttpResponse
from django.urls import reverse

from .sitemaps import PUBLIC_SITEMAPS


def robots_txt(request):
    sitemap_base = f"https://{request.get_host()}"
    content = f"""User-agent: *
Allow: /

Disallow: /dashboard/
Disallow: /signin/
Disallow: /signup/

Sitemap: {sitemap_base}{reverse('sitemap')}
Sitemap: {sitemap_base}{reverse('sitemap_txt')}
"""

    return HttpResponse(content, content_type="text/plain")


def sitemap_txt(request):
    sitemap_base = f"https://{request.get_host()}"
    urls = []
    for sitemap_class in PUBLIC_SITEMAPS.values():
        sitemap = sitemap_class()
        urls.extend(
            f"{sitemap_base}{sitemap.location(item)}"
            for item in sitemap.items()
        )

    return HttpResponse(
        "\n".join(dict.fromkeys(urls)) + "\n",
        content_type="text/plain",
    )