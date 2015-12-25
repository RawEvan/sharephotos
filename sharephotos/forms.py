from django import forms

class photoForm(forms.Form):
    photoFile = forms.ImageField()
    description = forms.CharField()
    tag = forms.CharField()
    