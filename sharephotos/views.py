#coding:utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from forms import photoInfoForm, searchForm, photoIDForm, photoFileForm, tagForm
from models import tb_photo_info, tb_tag
from PIL import Image
from faceControl import searchFaceset, addPhotoFaces
import time
import json
import dbControl
import cookiesControl
import pdb
import uploadImg
import common
# Create your views here.

def homepage(request):
    #pdb.set_trace()
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            search_word = request.POST['search_word']
            photo_list = dbControl.getRelatedPhotos(search_word, method = 'tag')
        else:
            pass
    search_word = u'奥运会'
    photo_list = dbControl.getRelatedPhotos(search_word, method = 'tag')        
    returnDict = {'photo_list': photo_list,
            'search_word': search_word,
            'latest_tag_list': latest_tag_list,
            'user_Email': Email}
    return  render(request, u'index.html', returnDict)

def upload(request):
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        try:
            Email = request.user.email
        except:
            Email = 'no Email'
        form = photoInfoForm(request.POST or None, request.FILES)
        if form.is_valid():
            photo_data = request.FILES['photoFile'].read()
            description = request.POST['description']
            tag = request.POST['tag']
            tag_list = tag.split(u'、')
            if 'sys_face' in tag_list:
                return render(request, u'抱歉，不能使用这个标签')
            # upload photo
            photo_url = uploadImg.objUpload(photo_data, tag) 
            thumbnail_url = common.get_thumbnail_url(photo_url, size = 'c_fit,w_750')
            # add face to faceset
            face_id_list = addPhotoFaces(method = 'url', urlOrPath = thumbnail_url)
            # save photo and tags
            dbControl.savePhotoAndTag(photo_url, description, tag_list, face_id_list, owner = Email) 
            # save info
            photo_info = dbControl.getPhotoInfo(photo_url, method = 'url')

            returnDict = {'latest_tag_list': latest_tag_list,
                    'user_Email': Email,
                    'photo_info': photo_info}
            return render(request, 'photo.html', returnDict)
        else:
            pass
    returnDict = {'latest_tag_list': latest_tag_list,
            'user_Email': Email}
    return render(request, u'upload.html', returnDict)
		
def formTag(request):
    #get search_word from the search form and check it, then redirects to view 'tag'
    form = searchForm(request.GET or None)
    photo_list = []
    search_word = ''
    if form.is_valid():
        search_word = request.GET['search_word']
    return HttpResponseRedirect(reverse('tag', args=[search_word]))

def tag(request, search_word):
    #search by tag (it's search_word here)
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    photo_list = dbControl.getRelatedPhotos(search_word, method = 'tag')        
    returnDict = {'photo_list': photo_list,
            'search_word': search_word,
            'user_Email': Email,
            'latest_tag_list': latest_tag_list}
    return render(request, u'index.html', returnDict)
        
def photo(request):
    # form = photoIDForm(request.GET or None) 
    # if form.is_valid():
    # don't check it temporary
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    p_id = int(request.GET['photo'])
    photo_info = dbControl.getPhotoInfo(p_id, method = 'p_id')
    returnDict = {'user_Email': Email,
            'latest_tag_list': latest_tag_list,
            'photo_info': photo_info}
    return render(request, 'photo.html', returnDict)
    
def face(request):
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        latest_tag_list = [r'none for now']
        form = photoFileForm(request.POST or None, request.FILES)
        if form.is_valid():
            photo_data = request.FILES['facePhotoFile'].read()
            tag = 'sys_face'
            photo_url = uploadImg.objUpload(photo_data, tag) # upload photo
            thumbnail_url = common.get_thumbnail_url(photo_url, size = 'c_fit,w_750')
            face_id_list = searchFaceset(method = 'url', urlOrPath = thumbnail_url)
            photo_list = []
            for face_id in face_id_list:
                each_face_photo_lsit = dbControl.getRelatedPhotos(face_id, method = 'tag')
                photo_list.extend(each_face_photo_lsit)         

            returnDict = {'photo_list': photo_list,
                    'user_Email': Email,
                    'latest_tag_list': latest_tag_list}
            return render(request, u'index.html', returnDict)
        else:
            pass
    returnDict = {'user_Email': Email,
            'latest_tag_list': latest_tag_list}
    return render(request, u'face.html', returnDict)

def photoManage(request):
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    try:
        Email = request.user.email
    except:
        Email = 'no Email'
    photo_list = dbControl.getRelatedPhotos(Email, method = 'owner')
    #super user owns photos without owner(or owned by 'system')
    if request.user.is_superuser:
        photo_list.extend(dbControl.getRelatedPhotos('system', method = 'owner'))
    returnDict = {'photo_list': photo_list,
            'owner': Email,
            'user_Email': Email,
            'latest_tag_list': latest_tag_list}
    return render(request, u'index.html', returnDict)


def delete(request, p_id):
    #delete photo, don't check user now
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.user.isauthenticated():
        p_id = int(p_id)
        is_deleted = dbControl.delete(p_id)
    else:
        is_deleted = False
    returnDict = {'user_Email': Email,
            'latest_tag_list': latest_tag_list,
            'is_deleted': is_deleted}
    return render(request, 'delete.html', returnDict)

def addTag(request):
    import pdb
    #pdb.set_trace()
    tag_list = []
    if request.method == 'GET':
    #check it later
        tag = request.GET['tag']
        p_id = int(request.GET['p_id'])
        tag_list = tag.split(u'、')
        if 'sys_face' in tag_list:
            return render(request, u'抱歉，不能使用这个标签')
        dbControl.addTag(p_id, tag_list, method = 'p_id')
        result = {'tag_list': tag_list, 'SUC': True}
        for eachTag in tag_list:
            if not dbControl.tagOfPhotoExist(eachTag, p_id):
                result['SUC'] = False
        return JsonResponse(result) 
    else:
        return JsonResponse('error')
