from django import forms


class photo_info_form(forms.Form):
    """ Use this form when upload photo. """
    photo_file = forms.ImageField()
    description = forms.CharField(max_length=300)
    tag = forms.CharField(max_length=10)
    permission = forms.CharField()


class search_form(forms.Form):
    """ Use this form when search. """
    search_word = forms.CharField(max_length=50)


class photo_id_form(forms.Form):
    """ Use this form when delete photo or get infomation of photo by ID. """
    p_id = forms.IntegerField()


class photo_file_form(forms.Form):
    """ Use this form when upload a photo to search. """
    face_photo_file = forms.ImageField()


class tag_form(forms.Form):
    """ don't use this now. """
    tag = forms.CharField(max_length=10)
    p_id = forms.IntegerField()
