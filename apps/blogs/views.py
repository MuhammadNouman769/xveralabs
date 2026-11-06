from django.http import Http404
from django.shortcuts import render

from .catalog import RESOURCES, get_resource

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

    resources = RESOURCES
    if active_filter in {"technology", "business", "industry"}:
        resources = [
            resource for resource in resources
            if resource["topic"] == active_filter
        ]
    elif active_filter in {"guides", "reports"}:
        kind = active_filter[:-1] if active_filter == "guides" else "report"
        resources = [
            resource for resource in resources
            if resource["kind"] == kind
        ]

    return render(
        request,
        "blogs/resource_index.html",
        {
            "resources": resources,
            "resource_filters": RESOURCE_FILTERS,
            "active_filter": active_filter,
            "featured_resource": RESOURCES[0],
            "playbooks": [resource for resource in RESOURCES if resource["kind"] == "guide"],
        },
    )


def resource_detail(request, slug):
    resource = get_resource(slug)
    if resource is None:
        raise Http404("Resource not found.")

    related = [
        item for item in RESOURCES
        if item["slug"] != resource["slug"]
        and (item["topic"] == resource["topic"] or item["kind"] == resource["kind"])
    ][:3]
    return render(
        request,
        "blogs/resource_detail.html",
        {"resource": resource, "related_resources": related},
    )
