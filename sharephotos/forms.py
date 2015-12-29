﻿from django import forms

class photoForm(forms.Form):
    photoFile = forms.ImageField()
    description = forms.CharField(max_length = 300)
    tag = forms.CharField(max_length = 10)

class searchForm(forms.Form):
    search_word = forms.CharField(max_length = 10)