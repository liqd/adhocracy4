import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):
    """Custom storage to store uploads in a subfolder called uploads"""

    location = os.path.join(settings.MEDIA_ROOT, "uploads")
    base_url = urljoin(settings.MEDIA_URL, "uploads/")
