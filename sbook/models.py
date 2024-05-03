from django.db import models

class Account(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
