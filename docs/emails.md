# Emails

adhocracy4 sends templated emails through `EmailBase` and its subclasses in
`adhocracy4/emails/`. Celery delivers them asynchronously via
`adhocracy4.emails.tasks.send_async`.

## Customising the From header

`EmailBase.dispatch()` uses `get_from_email()` when building each message. The
default implementation returns Django's `DEFAULT_FROM_EMAIL` setting (configure
this in your project's settings, e.g. production `local.py`).

Subclass `Email` (or a project-specific base class) and override
`get_from_email()` to set a display name or a different sender address — no need
to copy `dispatch()`.

Example:

```python
from email.utils import formataddr, parseaddr
from django.conf import settings
from adhocracy4.emails import Email


class ProjectEmail(Email):
    def get_from_email(self):
        _, address = parseaddr(settings.DEFAULT_FROM_EMAIL)
        return formataddr(("My platform", address))
```

Other hooks on `EmailBase` include `get_reply_to()`, `get_receivers()`, and
`get_organisation()`.

## Attachments

Optional inline images (e.g. logo) are configured via the `A4_EMAIL_ATTACHMENTS`
setting — see the changelog.
