from django.dispatch import Signal

"""Signal which is called after a user participated in a poll. The signal
receives the following arguments:
    poll: Poll
    creator: User
    content_id: uuid4
"""
poll_voted = Signal()
