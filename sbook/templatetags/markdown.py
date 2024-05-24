import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown as md

register = template.Library()

re_icon = re.compile(r"\:icon\:\`(brands|regular|solid)\:([\w-]+)\`")


@register.filter(is_safe=True, name='markdown')
@stringfilter
def markdown(text):
    for style, name in re_icon.findall(text):
        text = text.replace(
            f':icon:`{style}:{name}`',
            f'![icon](/static/svgs/{style}/{name}.svg)',
        )
    html = md.markdown(str(text))
    return mark_safe('<div class="markdown">' + html + '</div>')
