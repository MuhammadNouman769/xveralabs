from django.core.management.base import BaseCommand

from apps.main.case_studies import INDUSTRY_CASE_STUDIES
from apps.main.models import IndustryCaseStudy, IndustryCaseStudyBlock


class Command(BaseCommand):
    help = "Create starter industry case studies; existing admin content is preserved."

    def handle(self, *args, **options):
        created_count = 0
        for order, entry in enumerate(INDUSTRY_CASE_STUDIES):
            case_study, created = IndustryCaseStudy.objects.get_or_create(
                slug=entry["slug"],
                defaults={
                    "name": entry["name"],
                    "eyebrow": entry["eyebrow"],
                    "title": entry["title"],
                    "summary": entry["summary"],
                    "image_url": entry["image"],
                    "image_alt": entry["image_alt"],
                    "challenge": entry["challenge"],
                    "approach": entry["approach"],
                    "order": order,
                },
            )
            created_count += int(created)
            for kind, key in (
                (IndustryCaseStudyBlock.Kind.CAPABILITY, "capabilities"),
                (IndustryCaseStudyBlock.Kind.CONSIDERATION, "considerations"),
            ):
                existing_titles = set(
                    case_study.blocks.filter(kind=kind).values_list(
                        "title", flat=True
                    )
                )
                blocks = []
                for index, item in enumerate(entry[key]):
                    if isinstance(item, tuple):
                        title, text = item
                    else:
                        title, text = f"Consideration {index + 1}", item
                    if title in existing_titles:
                        continue
                    blocks.append(
                        IndustryCaseStudyBlock(
                            case_study=case_study,
                            kind=kind,
                            title=title,
                            text=text,
                            order=index,
                        )
                    )
                IndustryCaseStudyBlock.objects.bulk_create(blocks)

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} industry case studies created "
                f"({len(INDUSTRY_CASE_STUDIES) - created_count} already existed)."
            )
        )
