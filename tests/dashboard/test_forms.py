import pytest

from apps.dashboard import forms


def test_add_users_from_email_regex():
    data = {'add_users': 'max@sdg.de, nina@dsgo.de,peter@qwrde'}
    form = forms.AddUsersFromEmailForm(data=data)

    assert not form.is_valid()
    assert 'add_users' in form.errors


@pytest.mark.django_db
def test_add_users_from_email(user):
    data = {'add_users': '%s,unknown@domain.tld' % user.email}
    form = forms.AddUsersFromEmailForm(data=data)

    assert form.is_valid()
    assert form.missing == ['unknown@domain.tld']
    assert form.cleaned_data['add_users'] == [user]
