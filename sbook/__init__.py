import markdown as md
from django.utils.safestring import mark_safe
from pathlib import Path
import re

icons = []
icon_dir = Path("staticfiles/static")
mention = re.compile(r"@(user|topic)\:([\d\w\-_]+)")
assert icon_dir.exists(), f"icon dir: {icon_dir=} not found"

for icn in icon_dir.glob("*.svg"):
    icons.append(icn.stem)


def markdown(text):
    html = md.markdown(text)
    for icon in icons:
        html = html.replace(
            f':{icon}:',
            f'<img src="/static/static/{icon}.svg" class="text-fit" />',
        )
    for m_type, name in mention.findall(text):
        if m_type == "user":
            html = html.replace(
                f"@user:{name}",
                (
                    f'<a href="/users/{name}/" style="color: blue;">'
                    f'<img src="/profile/{name}.png" class="text-fit" />'
                    f'{name}</a>'
                )
            )
    return mark_safe(html)
