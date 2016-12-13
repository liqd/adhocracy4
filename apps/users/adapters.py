import re

from allauth.account.adapter import DefaultAccountAdapter

from apps.users import USERNAME_INVALID_MESSAGE
from apps.users import USERNAME_REGEX


class AccountAdapter(DefaultAccountAdapter):
    username_regex = re.compile(USERNAME_REGEX)
    error_messages = dict(
        DefaultAccountAdapter.error_messages,
        invalid_username=USERNAME_INVALID_MESSAGE
    )
