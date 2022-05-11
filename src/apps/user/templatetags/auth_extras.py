from django import template
from django.contrib.auth.models import Group 
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    try:
        group = Group.objects.get(name=group_name) 
    except ObjectDoesNotExist:
        group = False
    
    return True if group in user.groups.all() else False

@register.filter(name='if_empty')
def if_empty(object, str): 
    if object:
        return object
    return str