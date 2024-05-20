from django.db import models

# Create your models here.

class Classroom(object):
	"""docstring for """
    name = models.ChatField(max_length=255)		
