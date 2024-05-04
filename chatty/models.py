from django.db import models

class ChattyUser(models.Model):
    #id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.name

class ChattyRoom(models.Model):
    #id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    admin = models.ForeignKey(ChattyUser, related_name="admins", on_delete=models.CASCADE)
    members = models.ManyToManyField(ChattyUser, related_name="rooms")
    creation_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ChattyTextMessage(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(ChattyUser, related_name="sent", on_delete=models.CASCADE)
    room = models.ForeignKey(ChattyRoom, related_name="messages", on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)


