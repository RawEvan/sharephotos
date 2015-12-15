from django.shortcuts import render
import uploadImg
# Create your views here.

def hello(request):
    returnInfo = uploadImg.upload()
    return render(request, u'index.html')
