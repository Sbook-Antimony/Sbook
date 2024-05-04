#gg
from django import forms

class CreateRoomForm(forms.Form):
    name = forms.CharField(label="name")

class SendMessageForm(forms.Form):
    content = forms.CharField(label="content")
