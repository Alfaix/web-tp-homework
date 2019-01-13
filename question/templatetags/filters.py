from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def bootstrap_truncate(value, size, autoescape=True):
    if autoescape:
        value = conditional_escape(value)
    if len(value) <= size:
        return value
    else:
        truncated = value[:size-2] + '..'
        return mark_safe(f'<span data-toggle="tooltip" data-placement="top" title="{value}">{truncated}</span>')
