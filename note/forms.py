from django import forms


class NoteUploadForm(forms.Form):
    file = forms.FileField(
        label="file",
    )