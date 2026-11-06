from django.conf import settings
from django.core.files.storage import FileSystemStorage


def private_storage():
    """CVs are stored OUTSIDE the public media folder, so nobody can open them by guessing a URL.
    Staff download them through the dashboard (see views.cv_download)."""
    return FileSystemStorage(location=settings.BASE_DIR / "private_media")