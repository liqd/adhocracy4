from django import template

register = template.Library()


@register.assignment_tag
def get_activity_icon(activity):
    if activity.type == 'comment':
        return 'comment'
    elif activity.type == 'item':
        return 'lightbulb-o'
    elif activity.type == 'phase' and activity.verb == 'schedule':
        return 'clock-o'
    else:
        return 'star'
