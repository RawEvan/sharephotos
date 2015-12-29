#coding:utf-8
from django.shortcuts import render
from forms import photoForm, searchForm
from models import tb_photo_info, tb_tag
import dbControl
from PIL import Image
import pdb
import uploadImg
# Create your views here.

def homepage(request):
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            search_word = request.POST['search_word']
            #pdb.set_trace()
            photo_list = dbControl.getRelatedPhotos(search_word)
            return render(request, 'index.html', {'photo_list': photo_list, 'search_word': search_word})
        else:
            pass
    search_word = u'奥运会'
    photo_list = dbControl.getRelatedPhotos(search_word)        
    return render(request, u'index.html', {'photo_list': photo_list, 'search_word': search_word})

def upload(request):
    if request.method == 'POST':
        form = photoForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photoData = request.FILES['photoFile'].read()
            description = request.POST['description']
            tag = request.POST['tag']
            storeUrl = uploadImg.objUpload(photoData, tag)
            dbControl.savePhotoAndTag(storeUrl, description, tag)
            return render(request, 'upload_ok.html', {'form_info' : form, 'storeUrl':       storeUrl})
        else:
            pass
    return render(request, u'upload.html')
		
