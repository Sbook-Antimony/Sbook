#gg
from django import forms

class SigninForm(forms.Form):
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password")

class SignupForm(forms.Form):
    name = forms.CharField(label="name")
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password")
class CreateRoomForm(forms.Form):
    name = forms.CharField(label="name")

class SendMessageForm(forms.Form):
    content = forms.CharField(label="content")
