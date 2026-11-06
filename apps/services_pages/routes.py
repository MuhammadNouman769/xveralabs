
"""
One line per service page:
slug -> (URL path, URL name)
"""

from .catalog import (
    AI_CATEGORIES,
    INDUSTRY_CATEGORIES,
    SERVICE_CATEGORIES,
    SOLUTION_CATEGORIES,
    build_ai_pages,
    build_catalog_pages,
    build_domain_pages,
)

SERVICE_ROUTES = {
    "strategy-and-consulting": (
        "strategy-and-consulting/",
        "strategy_and_consulting",
    ),
    "business-optimization-consulting": (
        "business-optimization-consulting/",
        "business_optimization_consulting",
    ),
    "product-strategy": (
        "product-strategy/",
        "product_strategy",
    ),
    "technology-strategy": (
        "technology-strategy/",
        "technology_strategy",
    ),
    "learning-and-development": (
        "learning-and-development/",
        "learning_and_development",
    ),
    "advanced-technology": (
        "advanced-technology/",
        "advanced_technology",
    ),
    "robotic-process-automation": (
        "robotic-process-automation/",
        "robotic_process_automation",
    ),
    "internet-of-things": (
        "internet-of-things/",
        "internet_of_things",
    ),
    "blockchain": (
        "blockchain/",
        "blockchain",
    ),
    "ar-vr": (
        "ar-vr/",
        "ar_vr",
    ),
}

for page in build_catalog_pages():
    slug = page["slug"]
    SERVICE_ROUTES[slug] = (f"{slug}/", slug.replace("-", "_"))

for page in build_ai_pages():
    slug = page["slug"]
    SERVICE_ROUTES[slug] = (f"{slug}/", slug.replace("-", "_"))

for categories, domain in (
    (SOLUTION_CATEGORIES, "solution"),
    (INDUSTRY_CATEGORIES, "industry"),
):
    for page in build_domain_pages(categories, domain):
        slug = page["slug"]
        SERVICE_ROUTES[slug] = (f"{slug}/", slug.replace("-", "_"))
