class NoteElt:
    pass
class NoteParent:
    def __init__(self, attrs={}):
        self.topics = []
        self.captions = []
        self.tables = []
        self.key_words = []
        self.definitions = []
        self.children = []
        self.attrs = attrs

    def add_child(self, elt):
        self.children.append(elt)
    add_text = add_child
    add_more = add_child
    def add_topic(self, topic):
        self.topics.append(topic)
        self.add_child(topic)
    def add_def(self, def_):
        self.definitions.append(def_)
        self.add_child(def_)

class NoteDocument(NoteParent):
    def __init__(self, attrs):
        super().__init__()

class NoteTopic(NoteParent):
    def __init__(self, parent, attrs):
        super().__init__()
        self.parent = parent
        self.meta_name = attrs.get("meta-name")
        self.name = attrs.get("name")

class NoteDefinition(NoteParent):
    def __init__(self, parent, attrs):
        super().__init__()
        self.parent = parent
        self.for_ = attrs.get("for")
        if self.for_ == "#parent" or self.for_ is None:
            self.meta_name = parent.meta_name

class NoteText():
    def __init__(self, text):
        self.text = text

class NoteMore(NoteParent):
    def __init__(self, parent, attrs):
        super().__init__(attrs)
