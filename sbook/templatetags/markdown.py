
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from .. import markdown as md

register = template.Library()


@register.filter(is_safe=True, name='markdown')
@stringfilter
def markdown(text):
    return md(text)


@register.filter(is_safe=True, name='icon')
@stringfilter
def icon(text):
    ty, n, *cl = text.split(' ')
    txt = f'<img src="/static/svg/{ty}/{n}.svg" class="{" ".join(cl)}" />'
    return mark_safe(txt)
