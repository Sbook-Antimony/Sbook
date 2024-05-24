import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown as md

register = template.Library()


@register.filter(is_safe=True, name='markdown')
@stringfilter
def markdown(text):
    text = text.replace(r":icon:`([\w-]+)`", "![$1](/icons/$1.svg)")
    md = md.markdown(str(text))
    return mark_safe(md)
