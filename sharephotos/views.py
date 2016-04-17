# coding:utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse

from faceControl import searchFaceset, addPhotoFaces
import forms
import dbControl
import storage
import common


def homepage(request):

    """
    Homepage of the website.
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        form = forms.searchForm(request.POST or None)
        if form.is_valid():
            search_word = request.POST['search_word']
            photo_list = dbControl.getPhotosOfTag(search_word, method='tag')
        else:
            pass
    search_word = u'奥运会'
    photo_list = dbControl.getPhotosOfTag(search_word, method='tag')

    returnDict = {'photo_list': photo_list,
                  'search_word': search_word,
                  'latest_tag_list': latest_tag_list,
                  'user_Email': Email}
    return render(request, u'index.html', returnDict)


def formTag(request):

    """
    Get search_word from the search form and check it, then redirects to
    view 'tag'.
    """

    form = forms.searchForm(request.GET or None)
    photo_list = []
    search_word = ''
    if form.is_valid():
        search_word = request.GET['search_word']
    return HttpResponseRedirect(reverse('tag', args=[search_word]))


def tag(request, search_word):

    """
    Search by tag (it's search_word here).
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    photo_list = dbControl.getPhotosOfTag(search_word, method='tag')

    returnDict = {'photo_list': photo_list,
                  'search_word': search_word,
                  'user_Email': Email,
                  'latest_tag_list': latest_tag_list}
    return render(request, u'index.html', returnDict)


def photo(request):

    """
    Show infomation of photo. Don't check the p_id temporary
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    p_id = int(request.GET['photo'])
    photo_info = dbControl.getPhotoInfo(p_id, method='p_id')

    returnDict = {'user_Email': Email,
                  'latest_tag_list': latest_tag_list,
                  'photo_info': photo_info}
    return render(request, 'photo.html', returnDict)


def upload(request):

    """
    Upload photo and infomation.
    """

    import pdb
    pdb.set_trace()
    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        try:
            Email = request.user.email
        except:
            Email = 'no Email'
        form = forms.photoInfoForm(request.POST or None, request.FILES)
        if form.is_valid():
            photo_file = request.FILES['photoFile'].read()
            description = request.POST['description']
            tag = request.POST['tag']
            permission = request.POST['permission']
            photo_info = common.uploadPhoto(photo_file, description, tag, permission, Email)

            returnDict = {'latest_tag_list': latest_tag_list,
                          'user_Email': Email,
                          'photo_info': photo_info}
            return render(request, 'photo.html', returnDict)
        else:
            pass

    returnDict = {'latest_tag_list': latest_tag_list,
                  'user_Email': Email}
    return render(request, u'upload.html', returnDict)


def face(request):

    """
    Search photos related to the face(s) in given photo.
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.method == 'POST':
        latest_tag_list = [r'none for now']
        form = forms.photoFileForm(request.POST or None, request.FILES)
        if form.is_valid():
            photo_file = request.FILES['facePhotoFile'].read()
            # upload photo
            photo_url = storage.objUpload(photo_file, tag)
            thumbnail_url = common.get_thumbnail_url(
                photo_url, size='c_fit,w_750')
            # add face to faceset
            face_id_list = faceControl.addPhotoFaces(method='url', urlOrPath=thumbnail_url)
            photo_list = dbControl.getRelatedPhotos(face_id_list)

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

    """
    Manage user's photo.
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    try:
        Email = request.user.email
    except:
        Email = 'no Email'
    photo_list = dbControl.getPhotosOfTag(Email, method='owner')

    returnDict = {'photo_list': photo_list,
                  'owner': Email,
                  'user_Email': Email,
                  'latest_tag_list': latest_tag_list}
    return render(request, u'index.html', returnDict)


def delete(request, p_id):

    """
    Delete photo, don't check owner now
    """

    latest_tag_list = dbControl.get_latest_tags()
    Email = common.getEmail(request)
    if request.user.is_authenticated():
        p_id = int(p_id)
        is_deleted = dbControl.delete(p_id)
    else:
        is_deleted = False

    returnDict = {'user_Email': Email,
                  'latest_tag_list': latest_tag_list,
                  'is_deleted': is_deleted}
    return render(request, 'delete.html', returnDict)


def addTag(request):

    """
    Add tag by AJAX.
    """

    tag_list = []
    if request.method == 'GET':
        # check it later
        tag = request.GET['tag']
        p_id = int(request.GET['p_id'])
        tag_list = tag.split(u'、')
        dbControl.addTag(p_id, tag_list, method='p_id')
        result = {'tag_list': tag_list, 'SUC': True}
        for eachTag in tag_list:
            if not dbControl.tagOfPhotoExist(eachTag, p_id):
                result['SUC'] = False
        return JsonResponse(result)
    else:
        return JsonResponse('error')
