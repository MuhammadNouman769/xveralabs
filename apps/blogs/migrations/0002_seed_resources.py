from django.db import migrations


def seed_resources(apps, schema_editor):
    Resource = apps.get_model("blogs", "Resource")
    from apps.blogs.catalog import RESOURCES

    for order, entry in enumerate(RESOURCES):
        Resource.objects.using(schema_editor.connection.alias).get_or_create(
            slug=entry["slug"],
            defaults={
                "title": entry["title"],
                "category": entry["category"],
                "topic": entry["topic"],
                "kind": entry["kind"],
                "read_time": entry["read_time"],
                "excerpt": entry["excerpt"],
                "image": entry["image"],
                "image_alt": entry["image_alt"],
                "sections": entry["sections"],
                "order": order,
                "is_published": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("blogs", "0001_initial")]

    operations = [migrations.RunPython(seed_resources, migrations.RunPython.noop)]
