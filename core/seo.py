from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        reverse("sitemap")
    )

    content = f"""User-agent: *
Allow: /

Disallow: /admin/
Disallow: /signin/
Disallow: /signup/

Sitemap: {sitemap_url}
"""

    return HttpResponse(
        content,
        content_type="text/plain"
    )
