import functools

import json
import textwrap

from django.http import HttpRequest
from django.http import HttpResponseRedirect

import sbook.accounts
import sbook.models

from pyoload import *
from . import models


class Tuple(tuple):
    @property
    def length(self):
        return len(self)


class Classroom(sbook.accounts.ModelInter):
    model = models.Classroom

    @functools.cached_property
    def js(self: "Classroom") -> dict[str]:
        return {
            "name": self.model.name,
            "description": self.model.description,
            "code_of_conduct": self.model.code_of_conduct,
            "teachers": [t.js for t in self.teachers],
            "students": [s.js for s in self.students],
            "admins": [a.js for a in self.admins],
            "members": [m.js for m in self.members],
        }

    @functools.cached_property
    def teachers(self):
        return Tuple(map(sbook.accounts.User, self.model.teachers.all()))

    @functools.cached_property
    def students(self):
        return Tuple(map(sbook.accounts.User, self.model.students.all()))

    @functools.cached_property
    def admins(self):
        return Tuple(map(sbook.accounts.User, self.model.admins.all()))

    @functools.cached_property
    def members(self):
        return Tuple(set(self.teachers + self.students + self.admins))
