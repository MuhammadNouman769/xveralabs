from .registry import SECTIONS


NAV_ICONS = {
    "services": "✳",
    "service-groups": "◉",
    "service-blocks": "▤",
    "industries": "◈",
    "industry-blocks": "▤",
    "resources": "▧",
    "expenses": "$",
    "contacts": "✉",
    "jobs": "◇",
    "job-applications": "▣",
    "team": "♙",
    "partner-applications": "⌘",
    "ambassador-cohorts": "◎",
    "ambassador-content": "▤",
    "ambassador-stories": "❞",
    "ambassador-applications": "♧",
    "users": "♙",
    "groups": "⚙",
}


def dashboard_navigation(request):
    if not getattr(request.user, "is_authenticated", False):
        return {}
    sections = [
        {
            "key": section.key,
            "title": section.title,
            "icon": NAV_ICONS.get(section.key, "•"),
        }
        for section in SECTIONS
        if not section.superuser_only or request.user.is_superuser
        if request.user.is_superuser
        or request.user.has_perm(
            f"{section.model._meta.app_label}.view_{section.model._meta.model_name}"
        )
    ]
    return {"nav_sections": sections}
