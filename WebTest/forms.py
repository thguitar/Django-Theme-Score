from django import forms


class VideoForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    theme = forms.CharField(widget=forms.TextInput())
