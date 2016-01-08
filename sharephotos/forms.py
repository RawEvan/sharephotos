from django import forms

class photoUploadForm(forms.Form):
    photoFile = forms.ImageField()
    description = forms.CharField(max_length = 300)
    tag = forms.CharField(max_length = 10)

class searchForm(forms.Form):
    search_word = forms.CharField(max_length = 50)
        
class photoForm(forms.Form):
    p_id = forms.IntegerField()
    
class facePhotoForm(forms.Form):
    facePhotoFile = forms.ImageField()