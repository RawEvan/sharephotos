#coding:utf-8
from django.shortcuts import render
from forms import photoForm, searchForm
from models import tb_photo_info, tb_tag
import dbControl
from PIL import Image
import pdb
import uploadImg
import common
# Create your views here.

def homepage(request):
    #pdb.set_trace()
    latest_tags = tb_tag.objects.all().order_by('-id')[:5]
    latest_tags_list = [object.tag for object in latest_tags]
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            search_word = request.POST['search_word']
            photo_list = dbControl.getRelatedPhotos(search_word)
            return render(request, 'index.html', {'photo_list': photo_list, 'search_word': search_word, 'latest_tags_list': latest_tags_list})
        else:
            pass
    search_word = u'奥运会'
    photo_list = dbControl.getRelatedPhotos(search_word)        
    return render(request, u'index.html', {'photo_list': photo_list, 'search_word': search_word, 'latest_tags_list': latest_tags_list})

def upload(request):
    if request.method == 'POST':
        form = photoForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photo_data = request.FILES['photoFile'].read()
            description = request.POST['description']
            tag = request.POST['tag']
            store_url = uploadImg.objUpload(photo_data, tag) # upload photo
            dbControl.savePhotoAndTag(store_url, description, tag) # save info
            thumbnail_url = common.get_thumbnail_url(store_url)
            return render(request, 'upload_ok.html', {'form_info' : form, 'thumbnail_url': thumbnail_url})
        else:
            pass
    return render(request, u'upload.html')
		
