from django import template

register = template.Library()


@register.filter
def phone_format(phone_string):
    return phone_string[:2] + "(" + phone_string[2:5] + ")" + phone_string[5:]


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
