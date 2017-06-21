from apps.contrib.signals import connect_proxy_signals

from .models import A4Action
from .models import Action

connect_proxy_signals(Action, A4Action)
