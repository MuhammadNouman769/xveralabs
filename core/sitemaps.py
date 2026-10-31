
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    page_names = [
        # Main pages
        "home",
        "about-us",
        "why_choose_us",
        "contact_us",
        "services",
        "projects",
        "blogs",
        "case_studies",
        "faqs",

        # Important services
        "sqa",
        "web_dev",
        "product_dev",
        "dev_ops",
        "staff_aug",

        # About XveraLabs
        "careeers",
        "life_at_xvera_labs",
        "people",
        "campus_ambassador_program",

        # Services app
        "strategy_and_consulting",
        "business_optimization_consulting",
        "product_strategy",
        "technology_strategy",
        "learning_and_development",
        "advanced_technology",
        "robotic_process_automation",
        "internet_of_things",
        "blockchain",
        "ar_vr",

        # Partners
        "partners",
        "partners_investors",
    ]

    def get_domain(self, site=None):
        return "xveralabs.pythonanywhere.com"

    def items(self):
        return self.page_names

    def location(self, item):
        return reverse(item)
