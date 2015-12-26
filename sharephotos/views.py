from django.shortcuts import render
import uploadImg
from forms import photoForm
from PIL import Image
import pdb
from models import tb_photo_info, tb_tag
# Create your views here.

def homepage(request):
    return render(request, u'index.html')

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
            return render(request, 'upload_ok.html', {'form_info' : form, 'storeUrl': storeUrl})
    return render(request, u'upload.html')
		
