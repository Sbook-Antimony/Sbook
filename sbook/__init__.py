import markdown as md
from django.utils.safestring import mark_safe
from pathlib import Path
import re


icons = []
icon_dir = Path("staticfiles/static")
mention = re.compile(r"@([\d\w\-_]+);")
emoji = re.compile(r":([\w\-]+):")
fawesome = re.compile(r":(fa-[\w\-]+):")
assert icon_dir.exists(), f"icon dir: {icon_dir=} not found"

for icn in icon_dir.glob("*.svg"):
    icons.append(icn.stem)


def markdown(text):
    import sbook.accounts

    html = md.markdown(text)
    for name in mention.findall(text):
        try:
            user = sbook.accounts.User.get(username=name)
        except sbook.accounts.User.DoesNotExistError:
            pass
        else:
            html = html.replace(
                f"@{name};",
                f"""\
                <div class="tooltip">
                    <a href="/users/{name}/" style="color: green;">
                        <img
                            src="/profile/{name}.png"
                            class="text-fit w3-circle"
                        />
                        {user.model.name}
                    </a>
                    <div hidden class="raw-markdown tooltip-text">
                        {user.model.bio}
                    </div>
                </div>
                """,
            )
    for icon in icons:
        html = html.replace(
            f":{icon};",
            f'<img src="/static/static/{icon}.svg" class="text-fit" />',
        )
    for classes in fawesome.findall(html):
        html = html.replace(
            f":{classes}:",
            f'<i class="text-fit fas {classes}"></i>',
        )
    for emojii in emoji.findall(html):
        html = html.replace(
            f":{emojii}:",
            (
                '<img src="https://www.webfx.com/assets/emoji-cheat-sheet/img'
                f'/graphics/emojis/{emojii}.png" class="text-fit emoji" '
                f'title="expressionless" alt="{emojii}" />'
            ),
        )
    return mark_safe(html)
