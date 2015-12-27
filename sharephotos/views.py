#coding:utf-8
from django.shortcuts import render
import uploadImg
from forms import photoForm, searchForm
from PIL import Image
import pdb
from models import tb_photo_info, tb_tag
# Create your views here.

def homepage(request):
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            search_word = request.POST['search_word']
            #pdb.set_trace()
            try:
                targetTag = tb_tag.objects.get(tag = search_word)
            except:
                targetTag = tb_tag.objects.get(tag = u'没有找到图片')
            result_photo = targetTag.photo.all()    # get photo related to the tag 
            
            photo_list = []
            for each_photo in result_photo:
                photo_dict = {'url': each_photo.store_url,
                'description': each_photo.description}
                photo_list.append(photo_dict)
            return render(request, 'index.html', {'photo_list': photo_list, 'search_word': search_word})
                
    return render(request, u'index.html')

def upload(request):
    if request.method == 'POST':
        form = photoForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photoData = request.FILES['photoFile'].read()
            storeUrl = uploadImg.objUpload(photoData, tag = request.POST['tag'])
            
            #seperate these later
            photoInfo = tb_photo_info(store_url = storeUrl, description = request.POST['description'])
            photoInfo.save()
            tagInfo = tb_tag.objects.get_or_create(tag = request.POST['tag'])[0]
            tagInfo.save()
            tagInfo.photo.add(photoInfo)
            
            print 'upload_done'
            return render(request, 'upload_ok.html', {'form_info' : form, 'storeUrl':       storeUrl})
    return render(request, u'upload.html')
		
