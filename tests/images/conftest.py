import pytest

from tests.images.factories import ImageFactory

@pytest.fixture
def image_factory():
    return  ImageFactory()
