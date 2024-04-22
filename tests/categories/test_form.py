import pytest

from adhocracy4.categories.forms import CategoryForm


@pytest.mark.django_db
def test_category_form_empty_name(area_settings):
    module = area_settings.module
    form = CategoryForm(
        module=module,
        data={
            "name": "",
        },
    )
    assert "name" in form.errors
    assert "icon" not in form.errors
    assert not form.is_valid()


@pytest.mark.django_db
def test_category_form_invalid_icon(area_settings):
    module = area_settings.module
    form = CategoryForm(
        module=module,
        data={"name": "category 1", "icon": "XX"},
    )
    assert "name" not in form.errors
    assert "icon" in form.errors
    assert not form.is_valid()


@pytest.mark.django_db
def test_category_form_empty_icon(area_settings):
    module = area_settings.module
    form = CategoryForm(
        module=module,
        data={"name": "category 1", "icon": ""},
    )
    assert "name" not in form.errors
    assert "icon" not in form.errors
    assert form.is_valid()


@pytest.mark.django_db
def test_category_form_valid_icon(area_settings):
    module = area_settings.module
    form = CategoryForm(
        module=module,
        data={"name": "category 1", "icon": "diamant"},
    )
    assert "name" not in form.errors
    assert "icon" not in form.errors
    assert form.is_valid()
