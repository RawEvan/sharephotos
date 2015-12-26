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
            photo_list = tb_tag.objects.get(tag = search_word)
            result = photo_list.photo.all()
            return render(request, 'index.html', {'store_url': result.get().store_url,      'search_word': search_word})
                
    return render(request, u'index.html', {'search_word': 'no search'})

def upload(request):
    if request.method == 'POST':
        form = photoForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photoData = request.FILES['photoFile'].read()
            storeUrl = uploadImg.objUpload(photoData)
            
            #seperate these later
            photoInfo = tb_photo_info(store_url = storeUrl, description = request.POST['description'])
            photoInfo.save()
            tagInfo = tb_tag(tag = request.POST['tag'])
            tagInfo.save()
            tagInfo.photo.add(photoInfo)
            
            print 'upload_done'
            return render(request, 'upload_ok.html', {'form_info' : form, 'storeUrl':       storeUrl})
    return render(request, u'upload.html')
		
