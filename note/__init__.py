import yaml, textwrap


class Note:
    def __init__(self, folder):
        self.folder = folder
        self.data = yaml.safe_load((folder / "meta.yaml").read_text())
        print(self.data["longdesc"])
        self.data["shortdesc"] = textwrap.shorten(self.data["longdesc"], 300)
        self.iconFile = folder / "icon.png"
