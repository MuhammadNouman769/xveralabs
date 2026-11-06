from django.http import Http404
from django.shortcuts import render

from .models import Resource

RESOURCE_FILTERS = [
    ("all", "All resources"),
    ("technology", "Technology"),
    ("business", "Business"),
    ("industry", "Industries"),
    ("guides", "Guides"),
    ("reports", "Reports"),
]


def resource_index(request):
    active_filter = request.GET.get("filter", "all")
    if active_filter not in {value for value, _ in RESOURCE_FILTERS}:
        active_filter = "all"

    published = Resource.objects.filter(is_published=True)
    resources = list(published)
    if active_filter in {"technology", "business", "industry"}:
        resources = [resource for resource in resources if resource.topic == active_filter]
    elif active_filter in {"guides", "reports"}:
        kind = active_filter[:-1] if active_filter == "guides" else "report"
        resources = [resource for resource in resources if resource.kind == kind]

    resource_entries = [resource.as_catalog_entry() for resource in resources]
    all_entries = [resource.as_catalog_entry() for resource in published]

    return render(
        request,
        "blogs/resource_index.html",
        {
            "resources": resource_entries,
            "resource_filters": RESOURCE_FILTERS,
            "active_filter": active_filter,
            "featured_resource": all_entries[0] if all_entries else None,
            "playbooks": [resource for resource in all_entries if resource["kind"] == "guide"],
        },
    )


def resource_detail(request, slug):
    resource = get_resource_entry(slug)
    if resource is None:
        raise Http404("Resource not found.")

    related = [
        item for item in Resource.objects.filter(is_published=True).exclude(slug=slug)
        if item.topic == resource["topic"] or item.kind == resource["kind"]
    ][:3]
    return render(
        request,
        "blogs/resource_detail.html",
        {
            "resource": resource,
            "related_resources": [item.as_catalog_entry() for item in related],
        },
    )


def get_resource_entry(slug):
    resource = Resource.objects.filter(slug=slug, is_published=True).first()
    return resource.as_catalog_entry() if resource else None
