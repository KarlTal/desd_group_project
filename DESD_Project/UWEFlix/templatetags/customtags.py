from django import template

from UWEFlix.models import UserProfile

register = template.Library()


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.simple_tag
def get_credits(user):
    profile = UserProfile.objects.get(user_obj=user)
    return profile.credits
