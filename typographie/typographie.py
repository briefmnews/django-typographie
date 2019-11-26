from django.utils.safestring import mark_safe

from .registry import all_filters


def typographie(text):
    for f in all_filters:
        text = f(text)

    return mark_safe(text)
