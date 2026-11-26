from django.dispatch import Signal

# Sent after a moderator saved status or official feedback from the dashboard.
# Receivers get the item and the acting user.
moderation_item_feedback_saved = Signal()
