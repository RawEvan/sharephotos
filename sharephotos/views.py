from django.shortcuts import render
import uploadImg
from forms import photoForm
from PIL import Image
import pdb
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
            #storeUrl = uploadImg.urlUpload()
            return render(request, 'upload_ok.html', {'form_info' : form, 'storeUrl': storeUrl})
    print 'no form'
    return render(request, u'upload.html')
		
