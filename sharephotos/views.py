#coding:utf-8
from django.shortcuts import render
from forms import photoUploadForm, searchForm, photoForm, facePhotoForm
from models import tb_photo_info, tb_tag
from PIL import Image
from faceControl import searchFaceset, addPhotoFaces
import dbControl
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
        form = photoUploadForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photo_data = request.FILES['photoFile'].read()
            description = request.POST['description']
            tag = request.POST['tag']
            tag_list = tag.split(u'、')
            if 'sys_face' in tag_list:
                return render(request, u'抱歉，不能使用这个标签哦亲')
            photo_url = uploadImg.objUpload(photo_data, tag) # upload photo
            thumbnail_url = common.get_thumbnail_url(photo_url, size = 'c_fit,w_750')
            face_id_list = addPhotoFaces(method = 'url', urlOrPath = thumbnail_url)
            dbControl.savePhotoAndTag(photo_url, description, tag_list, face_id_list) # save info
            photo_info = dbControl.getPhotoInfo(method = 'url', search_word = photo_url)
            return render(request, 'photo_info.html', {'photo_info' : photo_info})
        else:
            pass
    return render(request, u'upload.html')
		
def tag(request):
    #pdb.set_trace()
    latest_tags = tb_tag.objects.all().order_by('-id')[:5]
    latest_tags_list = [object.tag for object in latest_tags]
    form = searchForm(request.GET or None)
    if form.is_valid():
        search_word = request.GET['search_word']
        photo_list = dbControl.getRelatedPhotos(search_word)
        return render(request, 'index.html', {'photo_list': photo_list, 'search_word': search_word, 'latest_tags_list': latest_tags_list})
    else:
        search_word = u'没有找到图片'
        photo_list = dbControl.getRelatedPhotos(search_word)        
        return render(request, u'index.html', {'photo_list': photo_list, 'search_word': search_word, 'latest_tags_list': latest_tags_list})
        
def photo(request):
    #pdb.set_trace()
    # form = photoForm(request.GET or None) 
    # if form.is_valid():
    # don't check it temporary
    p_id = int(request.GET['photo'])
    photo_info = dbControl.getPhotoInfo(method = 'p_id', search_word = p_id)
    return render(request, 'photo_info.html', {'photo_info' : photo_info})
    
def face(request):
    #pdb.set_trace()
    if request.method == 'POST':
        latest_tags_list = [r'none for now']
        form = facePhotoForm(request.POST or None, request.FILES)
        #pdb.set_trace()
        if form.is_valid():
            photo_data = request.FILES['facePhotoFile'].read()
            tag = 'sys_face'
            photo_url = uploadImg.objUpload(photo_data, tag) # upload photo
            thumbnail_url = common.get_thumbnail_url(photo_url, size = 'c_fit,w_750')
            face_id_list = searchFaceset(method = 'url', urlOrPath = thumbnail_url)
            photo_list = []
            for face_id in face_id_list:
                each_face_photo_lsit = dbControl.getRelatedPhotos(search_word = face_id)
                photo_list.extend(each_face_photo_lsit)         
            return render(request, u'index.html', {'photo_list': photo_list,'latest_tags_list': latest_tags_list})
        else:
            pass
    return render(request, u'face.html')