from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from . import models
from .forms import AddUserAdminForm
from .forms import UserAdminForm


class UserAdmin(auth.admin.UserAdmin):
    form = UserAdminForm
    add_form = AddUserAdminForm
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "groups")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser")}),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "get_newsletters")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("date_joined", "last_login", "get_newsletters")
    list_display = (
        "id",
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_staff",
        "is_superuser",
        "get_newsletters",
    )
    list_filter = ("is_staff", "is_superuser", "last_login")
    search_fields = ("username", "email", "id")


class GroupAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)


admin.site.register(models.User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
