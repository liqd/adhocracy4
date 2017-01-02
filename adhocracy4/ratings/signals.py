from django.conf import settings
from adhcoracy4 import generics

from .models import Rating

generics.setup_delete_signals(settings.A4_RATEABLES, Rating)
