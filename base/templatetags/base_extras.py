from django import template

register = template.Library()

@register.filter
def subtract_len(value, arg):
    return len(value) - len(arg)