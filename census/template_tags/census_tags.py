
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def to_s(mixed):
    return str(mixed)

@register.filter
def percent(num, denom):
    return round((num * 100) / denom)
