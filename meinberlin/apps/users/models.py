from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.organisations.models import Organisation

from . import USERNAME_INVALID_MESSAGE
from . import USERNAME_REGEX


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_("Your username will appear publicly next to your posts."),
        validators=[
            validators.RegexValidator(
                USERNAME_REGEX, USERNAME_INVALID_MESSAGE, "invalid"
            )
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
            "used_as_email": _(
                "This username is already used as an " "e-mail address."
            ),
        },
    )

    email = models.EmailField(
        _("Email address"),
        unique=True,
        error_messages={"unique": _("A user with that email address already exists.")},
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(editable=False, default=timezone.now)

    get_notifications = models.BooleanField(
        verbose_name=_("Notifications"),
        default=True,
        help_text=_(
            "Yes, I would like to be notified by e-mail about the start "
            "and end of participation opportunities. This applies to all "
            "projects I follow. I also receive an e-mail when someone "
            "comments on one of my contributions."
        ),
    )

    get_newsletters = models.BooleanField(
        verbose_name=_("Newsletter"),
        default=False,
        help_text=_(
            "Yes, I would like to receive e-mail newsletters about "
            "the projects I am following."
        ),
    )

    objects = auth_models.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def organisations(self):
        initiator_orgs = self.organisation_set.all()
        if self.groups.all():
            user_groups = self.groups.all().values_list("id", flat=True)
            group_orgs = Organisation.objects.filter(groups__in=user_groups)
            orgs = initiator_orgs | group_orgs
            return orgs.distinct()
        return initiator_orgs

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = "%s <%s>" % (self.username, self.email)
        return full_name.strip()

    def signup(self, username, email, commit=True):
        """Update the fields required for sign-up."""
        self.username = username
        self.email = email
        if commit:
            self.save()
