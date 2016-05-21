# coding:utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse

from faceControl import add_faces
import forms
import dbControl
import storage
import common


def homepage(request):
    """
    Homepage of the website.
    """

    latest_tag_list = dbControl.get_latest_tags()
    email = common.get_email(request)
    if request.user.is_authenticated():
        # if search
        if request.method == 'POST':
            form = forms.search_form(request.POST or None)
            if form.is_valid():
                search_word = request.POST['search_word']
                photo_list = dbControl.get_photos_of_tag(search_word)
            else:
                pass
        # not search, get photos may be interested in
        else:
            search_word= ''
            photo_list = dbControl.get_interested_photos(email=email)
    # not login
    else:
        search_word = ''
        photo_list = dbControl.get_latest_photos()

    return_dict = {'photo_list': photo_list,
                  'search_word': search_word,
                  'latest_tag_list': latest_tag_list,
                  'user_Email': email}
    return render(request, u'index.html', return_dict)


def search(request):
    """
    Get search_word from the search form and check it, then redirects to
    view 'tag'.
    """

    form = forms.search_form(request.GET or None)
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
    email = common.get_email(request)
    photo_list = dbControl.get_photos_of_tag(search_word)

    return_dict = {'photo_list': photo_list,
                  'search_word': search_word,
                  'user_Email': email,
                  'latest_tag_list': latest_tag_list}
    return render(request, u'index.html', return_dict)


def photo(request):
    """
    Show infomation of photo. Don't check the p_id temporary
    """

    latest_tag_list = dbControl.get_latest_tags()
    email = common.get_email(request)
    p_id = int(request.GET['photo'])
    photo_info = dbControl.get_photo_info(p_id, method='p_id')
    is_collected = dbControl.is_collected(email, p_id)
    return_dict = {'user_Email': email,
                  'latest_tag_list': latest_tag_list,
                  'is_collected':is_collected,
                  'photo_info': photo_info}
    return render(request, 'photo.html', return_dict)


def upload(request):
    """
    Upload photo and infomation.
    """
    if request.user.is_authenticated():
        latest_tag_list = dbControl.get_latest_tags()
        email = common.get_email(request)

        # after upload
        if request.method == 'POST':
            form = forms.photo_info_form(request.POST or None, request.FILES)
            if form.is_valid():
                photo_file = request.FILES['photo_file'].read()
                description = request.POST['description']
                tag = request.POST['tag']
                permission = request.POST['permission']
                photo_info = common.upload_photo(
                    photo_file, description, tag, permission, email)

                return_dict = {'latest_tag_list': latest_tag_list,
                              'user_Email': email,
                              'photo_info': photo_info}
                return render(request, 'photo.html', return_dict)
            else:
                pass
        # before upload
        else:
            return_dict = {'latest_tag_list': latest_tag_list,
                          'user_Email': email}
            return render(request, u'upload.html', return_dict)
    else:
        return HttpResponseRedirect(reverse('users_login'))



def face_search(request):
    """
    Search photos related to the face(s) in given photo.
    """

    latest_tag_list = dbControl.get_latest_tags()
    email = common.get_email(request)
    if request.method == 'POST':
        latest_tag_list = [r'none for now']
        form = forms.photo_file_form(request.POST or None, request.FILES)
        if form.is_valid():
            photo_file = request.FILES['face_photo_file'].read()
            # upload photo
            photo_url = storage.objUpload(photo_file, tag)
            thumbnail_url = common.get_thumbnail_url(
                photo_url, size='c_fit,w_750')
            # add face to faceset
            person_id_list = faceControl.add_faces(
                method='url', urlOrPath=thumbnail_url)
            photo_list = dbControl.get_related_photos(person_id_list)

            return_dict = {'photo_list': photo_list,
                          'user_Email': email,
                          'latest_tag_list': latest_tag_list}
            return render(request, u'index.html', return_dict)
        else:
            pass

    return_dict = {'user_Email': email,
                  'latest_tag_list': latest_tag_list}
    return render(request, u'face.html', return_dict)


def photo_manage(request):
    """ Manage user's photo. """
    if request.user.is_authenticated():
        latest_tag_list = dbControl.get_latest_tags()
        email = common.get_email(request)
        photo_list = dbControl.get_owned_photos(email)

        return_dict = {'photo_list': photo_list,
                      'owner': email,
                      'user_Email': email,
                      'latest_tag_list': latest_tag_list}
        return render(request, u'index.html', return_dict)
    else:
        return HttpResponseRedirect(reverse('users_login'))


def photo_delete(request, p_id):
    """ Delete photo, don't check owner now. """
    latest_tag_list = dbControl.get_latest_tags()
    email = common.get_email(request)
    if request.user.is_authenticated():
        p_id = int(p_id)
        is_deleted = dbControl.delete(p_id)
    else:
        is_deleted = False

    return_dict = {'user_Email': email,
                  'latest_tag_list': latest_tag_list,
                  'is_deleted': is_deleted}
    return render(request, 'delete.html', return_dict)


def tag_add(request):
    """
    Add tag by AJAX.
    """
    if request.user.is_authenticated():
        tag_list = []
        if request.method == 'GET':
            # check it later
            tag = request.GET['tag']
            p_id = int(request.GET['p_id'])
            tag_list = tag.split(u'、')
            dbControl.add_tag(p_id, tag_list, method='p_id')
            result = {'tag_list': tag_list, 'SUC': True}
            for eachTag in tag_list:
                if not dbControl.tagOfPhotoExist(eachTag, p_id):
                    result['SUC'] = False
            return JsonResponse(result)
    else:
        return JsonResponse('error')


def collect_add(request):
    """ Add collected photo for user. """
    if request.user.is_authenticated():
        email = common.get_email(request)
        if request.method == 'GET':
            return_dict = {}
            photo_id = int(request.GET['p_id'])
            return_dict['SUC'] = dbControl.add_collect(email, photo_id)
            return_dict['collected_times'] = dbControl.get_collected_times(photo_id)
            return JsonResponse(return_dict)
    else:
        return HttpResponseRedirect(reverse('users_login'))


def collect_delete(request):
    """ Cancel collect. """
    if request.user.is_authenticated():
        email = common.get_email(request)
        if request.method == 'GET':
            photo_id = int(request.GET['p_id'])
            if dbControl.cancel_collect(email, photo_id):
                collected_times = dbControl.get_collected_times(photo_id)
                return JsonResponse({'SUC':True, 'collected_times':collected_times})
            else:
                return JsonResponse({'SUC':False})
    else:
        return HttpResponseRedirect(reverse('users_login'))


def user_info(request):
    """ Show infomation of user. """
    if request.user.is_authenticated():
        email = common.get_email(request)
        info = dbControl.get_user_info(email)

        return_dict = {
                'user_Email': email,
                'info': info,
                }
        return render(request, 'user_info.html', return_dict)
    else:
        return HttpResponseRedirect(reverse('users_login'))
