from django import forms


class photoInfoForm(forms.Form):
    photoFile = forms.ImageField()
    description = forms.CharField(max_length=300)
    tag = forms.CharField(max_length=10)


class searchForm(forms.Form):
    search_word = forms.CharField(max_length=50)


class photoIDForm(forms.Form):
    p_id = forms.IntegerField()


class photoFileForm(forms.Form):
    facePhotoFile = forms.ImageField()


class tagForm(forms.Form):
    tag = forms.CharField(max_length=10)
    p_id = forms.IntegerField()
