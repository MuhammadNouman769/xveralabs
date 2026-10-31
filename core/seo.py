from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /signin/
Disallow: /signup/

Sitemap: https://xveralabs.pythonanywhere.com/sitemap.xml
"""

    return HttpResponse(content, content_type="text/plain")