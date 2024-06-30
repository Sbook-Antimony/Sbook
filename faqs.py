from pyoload import *
import yaml


def get_faqs():
    return Faq.INSTANCES


def create(*args, **kw):
    model = FaqModel(**kw)
    model.save()
    return Faq(model)


class Faq:
    INSTANCES = []

    @annotate
    def __init__(self, questions: list[str], answer: str):
        self.questions = questions
        self.answer = answer
        self.INSTANCES.append(self)


with open("faqs.yaml") as f:
    text = f.read()
    data = yaml.safe_load(text)
    for questions, answer in data:
        Faq(questions, answer)
