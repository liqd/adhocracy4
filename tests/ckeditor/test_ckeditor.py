from django.conf import settings

from adhocracy4.ckeditor.storage import CustomStorage


def test_ckeditor_storage_backend():
    storage = CustomStorage()
    assert storage.path("test.txt").endswith(settings.MEDIA_ROOT + "/uploads/test.txt")
