import hashlib
import secrets
import string

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from adhocracy4.models import base
from adhocracy4.modules.models import Module


def get_token(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


# only used by migration
def get_token_12():
    return get_token(12)


def get_token_16():
    return get_token(16)


class TokenSalt(models.Model):
    salt = models.CharField(
        default=get_token_16, max_length=16, editable=False, unique=True
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        for i in range(4):
            try:
                super().save(*args, **kwargs)
                return
            except IntegrityError as e:
                if "UNIQUE constraint failed" in e.args[0]:
                    if i == 3:
                        raise
                    else:
                        self.salt = get_token_16()
                else:
                    raise

    @staticmethod
    def get_or_create_salt_for_module(module):
        try:
            token_salt = TokenSalt.objects.get(module=module)
        except TokenSalt.DoesNotExist:
            token_salt = TokenSalt.objects.create(module=module)
        return token_salt.salt


class TokenPackage(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()
    downloaded = models.BooleanField(default=False)

    class Meta:
        ordering = ["pk"]

    @property
    def num_tokens(self):
        return VotingToken.objects.filter(package=self).count()

    @property
    def is_created(self):
        return self.num_tokens == self.size

    @staticmethod
    def get_sum_token(module):
        num_tokens = (
            TokenPackage.objects.filter(module=module)
            .aggregate(Sum("size"))
            .get("size__sum")
        )
        if num_tokens is None:
            num_tokens = 0
        return num_tokens


class VotingToken(models.Model):
    token = models.CharField(
        max_length=40, default=get_token_16, blank=True, editable=False
    )
    token_hash = models.CharField(max_length=128, editable=False, unique=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    allowed_votes = models.PositiveSmallIntegerField(default=5)
    package = models.ForeignKey(TokenPackage, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this token should be treated as "
            "active. Unselect this instead of deleting tokens."
        ),
    )

    # if token already exists, try to generate another one
    def save(self, *args, **kwargs):
        for i in range(4):
            try:
                super().save(*args, **kwargs)
                return
            except IntegrityError as e:
                if "UNIQUE constraint failed" in e.args[0]:
                    if i == 3:
                        raise
                    else:
                        self.token = get_token_16()
                        self.token_hash = self.hash_token(self.token, self.module)
                else:
                    raise

    @property
    def votes(self):
        return TokenVote.objects.filter(token=self)

    @property
    def num_votes_left(self):
        num_votes = self.votes.count()
        return self.allowed_votes - num_votes

    @property
    def has_votes_left(self):
        return self.num_votes_left > 0

    @property
    def project(self):
        return self.module.project

    def is_valid_for_item(self, item):
        return item.module == self.module

    @staticmethod
    def hash_token(token, module):
        salt = TokenSalt.get_or_create_salt_for_module(module)
        token_hash = hashlib.sha3_512((salt + token).encode()).hexdigest()
        return token_hash

    @staticmethod
    def get_voting_token(token, module_id):
        try:
            module = Module.objects.get(id=module_id)
            token_hash = VotingToken.hash_token(token, module)
            return VotingToken.objects.get(token_hash=token_hash)
        except (
            Module.DoesNotExist,
            Module.MultipleObjectsReturned,
            VotingToken.DoesNotExist,
            VotingToken.MultipleObjectsReturned,
        ):
            return None

    @staticmethod
    def get_voting_token_by_hash(token_hash, module):
        try:
            return VotingToken.objects.get(token_hash=token_hash, module=module)
        except (VotingToken.DoesNotExist, VotingToken.MultipleObjectsReturned):
            return None

    def __str__(self):
        return "{}-{}-{}-{}".format(
            self.token[0:4], self.token[4:8], self.token[8:12], self.token[12:16]
        )


class TokenVote(base.TimeStampedModel):
    token = models.ForeignKey(VotingToken, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        unique_together = ("content_type", "object_pk", "token")
        indexes = [models.Index(fields=["content_type", "object_pk"])]

    def clean(self, *args, **kwargs):
        if not self.token.is_valid_for_item(self.content_object):
            raise ValidationError(
                {"token": _("This token is not valid for this project.")}
            )
        elif not self.token.is_active:
            raise ValidationError({"token": _("This token is not active.")})
        elif not self.token.has_votes_left:
            raise ValidationError({"token": _("This token has no votes left.")})
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
