from django.views.generic.detail import DetailView

from . import models


class ProfileView(DetailView):
    model = models.User
    slug_field = 'username'
