import functools

import json
import textwrap

from django.http import HttpRequest
from django.http import HttpResponseRedirect

import sbook.accounts
import sbook.models

from pyoload import *
from . import models
from sbook.accounts import *


class Tuple(tuple):
    @property
    def length(self):
        return len(self)

