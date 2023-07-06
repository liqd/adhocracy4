import pytest

from adhocracy4.categories.models import CategoryAlias


@pytest.mark.django_db
def test_str_category(category):
    assert str(category) == category.name


@pytest.mark.django_db
def test_str_category_alias(category_alias):
    assert str(category_alias) == category_alias.title


@pytest.mark.django_db
def test_get_category_alias(module, category_factory, category_alias_factory):
    category_factory(module=module)
    assert not CategoryAlias.get_category_alias(module)

    category_alias = category_alias_factory(module=module)
    assert CategoryAlias.get_category_alias(module) == category_alias
