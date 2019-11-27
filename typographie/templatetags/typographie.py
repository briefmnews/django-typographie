from django import template
from django.template.defaultfilters import stringfilter
from ..typographie import typographie as typographie_func

register = template.Library()


@register.filter
@stringfilter
def typographie(text):
    return typographie_func(text)


typographie.is_safe = True
