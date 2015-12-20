from django.shortcuts import render
import uploadImg
# Create your views here.

def homepage(request):
    return render(request, u'index.html')

#def upload(request, ):
		