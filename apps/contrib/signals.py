from django.db.models.signals import m2m_changed
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

signals = [
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
]


def _make_sender_fn(model, signal):
    """Make a sender function used to connect signals."""
    def sender_fn(sender, **kwargs):
        # signal send method passes itself as a signal kwarg to its receivers
        kwargs.pop('signal')
        signal.send(sender=model, **kwargs)

    return sender_fn


def connect_proxy_signals(from_model, to_model):
    """Connect all signals from a Proxy model to its parent.

    There is 9 year old bug report where the problem is discussed:
    https://code.djangoproject.com/ticket/9318
    """
    for signal in signals:
        signal.connect(
            _make_sender_fn(to_model, signal),
            sender=from_model,
            weak=False,
        )
