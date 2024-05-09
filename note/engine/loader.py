from pathlib import Path

from . import objects, exceptions
from html.parser import HTMLParser
class NotesParser(HTMLParser):
    workingdir:Path
    def __init__(self, workdir):
        super().__init__()
        self.workingdir = Path(workdir)
        self.documents = []
        self.scope = []

    def handle_startendtag(self, tag, attrs):
        pass
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tuple(tag.split(":"))
        match tag:
            case ("note",):
                self.document = objects.NoteDocument(attrs)
                self.scope = [self.document]
                self.documents.append(self.document)
            case ("topic",):
                self.topic = [objects.NoteTopic(self.scope[-1], attrs)]
                self.document.add_topic(self.topic[-1])
                self.scope.append(self.topic[-1])
            case ("definition", ):
                def_ = objects.NoteDefinition(self.scope[-1], attrs)
                self.scope[-1].add_def(def_)
                self.scope.append(def_)
            case ('more', ):
                more = objects.NoteMore(self.scope[-1], attrs)
                self.scope[-1].add_more(more)
                self.scope.append(more)
            case a:
                raise exceptions.TagDoesNotExistsException(a)

    def handle_data(self, txt):
        if txt.isspace():
            return
        print('data:', txt)
        ret = "\n".join(line.strip() for line in txt.splitlines())
        self.scope[-1].add_text(objects.NoteText(ret))
    def handle_endtag(self, name):
        self.scope.pop()
    def parse(self):
        #super().parse()
        self.feed((self.workingdir/"index.note").read_text())
        return self


def parse_notes(url):
    url = Path(url)
    documents = NotesParser(url).parse().documents
    return documents

