import markdown as md
from django.utils.safestring import mark_safe
import re

re_icon = re.compile(r"\:icon\:\`(brands|regular|solid)\:([\w-]+)\`")


def markdown(text):
    for style, name in re_icon.findall(text):
        text = text.replace(
            f':icon:`{style}:{name}`',
            f'![icon](/static/svg/{style}/{name}.svg)',
        )
    html = md.markdown(str(text))
    return mark_safe('<div class="markdown">' + html + '</div>')
