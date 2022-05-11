from django import template

register = template.Library()


@register.filter
def in_type(obj, xyz_type):
    return obj.filter(type=xyz_type)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)
