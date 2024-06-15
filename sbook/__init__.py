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
    import sbook.accounts

    html = md.markdown(text)
    for icon in icons:
        html = html.replace(
            f':{icon}:',
            f'<img src="/static/static/{icon}.svg" class="text-fit" />',
        )
    for m_type, name in mention.findall(text):
        if m_type == "user":
            try:
                user = sbook.accounts.User.get(username=name)
            except sbook.accounts.User.DoesExistError:
                pass
            else:
                html = html.replace(
                    f"@user:{name}",
                    f"""\
                    <div class="tooltip">
                        <a href="/users/{name}/" style="color: green;">
                            <img
                                src="/profile/{name}.png"
                                class="text-fit w3-circle"
                            />
                            {user.model.name}
                        </a>
                        <div class="raw-markdown tooltip-text">
                            {user.model.bio}
                        </div>
                    </div>
                    """,
                )
    return mark_safe(html)

