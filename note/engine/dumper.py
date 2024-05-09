import os
from pathlib import Path
import shutil

from . import objects, assets
from note import *
class Tag(list):
    def __init__(self, _parent, _name, _attrs={}, **kw):
        self.name = _name
        self.attrs = {x[1:] if x[0]=='_' else x: y for x, y in (_attrs|kw).items()}


        self.child = _parent is not None
        if self.child:
            _parent.append(self)
        super().__init__()
    def render(self, inchr):
        print("rendering", self.name, self.child)
        txt = f"<{self.name}"
        for a, v in self.attrs.items():
            txt += f' {a}="{v}"'
        txt +=">\n"

        for child in self:
            txt += child.render(inchr)
        txt += f"\n</{self.name}>"
        ret = ""
        if self.child:
            for ln in txt.splitlines():
                ret += inchr+ln+"\n"
            return ret
        return txt

def clear(dir):
    if dir.is_dir():
        for x in dir.glob("*"):
            clear(x)
        dir.rmdir()
    else:
        dir.unlink()
class TTag(Tag):
    def __init__(self, parent, txt):
        parent.append(self)
        self.text = txt
    def render(self, inchr):
        return ("\n").join(inchr+ln for ln in self.text.splitlines())
class OTag(Tag):
    def render(self, inchr):
        txt = inchr+f"<{self.name}"
        for a, v in self.attrs.items():
            txt += f' {a}="{v}"'
        txt +=" />\n"
        return txt
def load_xml(doc):
    root = Tag(None,"html", lang=doc.attrs.get('lang'))
    head = Tag(root, "head")
    OTag(head, "meta", charset="utf-8")
    OTag(head, "meta", name="viewport", content="width=device-width, initial-scale=1.0")
    OTag(head, "link", rel="stylesheet", href="css/note.css")
    Tag   (head, "script", src='js/note.js')

    body = Tag(root, "body")
    recur_render(body, doc)
    return root.render('    ')

def recur_render(elt, doc):
    print("recur_render:", elt, doc)
    match doc.__class__:
        case objects.NoteDocument:
            for child in doc.children:
                recur_render(elt, child)
        case objects.NoteTopic:
            TTag(Tag(section:=Tag(elt, "section",_class="note-NoteTopic"), "h1", id="topic:"+doc.meta_name), doc.name)
            for child in doc.children:
                recur_render(section, child)
        case objects.NoteDefinition:
            main = Tag(elt, "div", _class="note-NoteDefinition")
            TTag(Tag(main, "h4", id="definition:"+doc.meta_name), doc.name if hasattr(doc, 'name') else "definition")
            for child in doc.children:
                recur_render(main, child)
        case objects.NoteText:
            TTag(elt, doc.text)
        case objects.NoteMore:
            more = nMore(elt, doc.attrs)
            for child in doc.children:
                recur_render(more.container, child)
        case a:
            raise ValueError(a, doc)

def nMore(p, kw):
    main = Tag(
        p,
        'div',
        _class = "nMore"
    )
    btn = Tag(main, "button")
    TTag(btn, kw.get("title", "more<hr>"))
    main.container = Tag(main, 'div')
    return main
def init_dir(_dir):
    if _dir.exists():
        clear(_dir)
    _dir.mkdir()
    css = _dir/"css"
    css.mkdir()
    ncss = css / "note.css"
    shutil.copy(assets.notecss, ncss)
    
    js = _dir/"js"
    js.mkdir()
    njs = js/"note.js"
    shutil.copy(assets.notejs, njs)
    
    imgf = assets.assets/'images'
    imgt = _dir/'images'
    shutil.copytree(imgf, imgt)

def dump_document(document, _dir):
    _dir = Path(_dir)
    init_dir(_dir)
    index = _dir / "index.html"
    index.touch()
    index.write_text(load_xml(document))
