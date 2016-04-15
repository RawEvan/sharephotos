from django import forms


class photoInfoForm(forms.Form):
    """ Use this form when upload photo. """
    photoFile = forms.ImageField()
    description = forms.CharField(max_length=300)
    tag = forms.CharField(max_length=10)


class searchForm(forms.Form):
    """ Use this form when search. """
    search_word = forms.CharField(max_length=50)


class photoIDForm(forms.Form):
    """ Use this form when delete photo or get infomation of photo by ID. """
    p_id = forms.IntegerField()


class photoFileForm(forms.Form):
    """ Use this form when upload a photo to search. """
    facePhotoFile = forms.ImageField()


class tagForm(forms.Form):
    """ don't use this now. """
    tag = forms.CharField(max_length=10)
    p_id = forms.IntegerField()
