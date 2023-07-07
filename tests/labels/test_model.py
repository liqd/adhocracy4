import pytest

from adhocracy4.labels.models import LabelAlias


@pytest.mark.django_db
def test_str_label(label):
    assert str(label) == label.name


@pytest.mark.django_db
def test_str_label_alias(label_alias):
    assert str(label_alias) == label_alias.title


@pytest.mark.django_db
def test_get_label_alias(module, label_factory, label_alias_factory):
    label_factory(module=module)
    assert not LabelAlias.get_label_alias(module)

    label_alias = label_alias_factory(module=module)
    assert LabelAlias.get_label_alias(module) == label_alias
