# coding:utf-8
# some common function
import storage
import dbControl
import faceControl


def get_thumbnail_url(original_url, size='w_250,h_150'):

    """ Get the url of the photo's thumbnail. """

    split_url = original_url.split('/')
    thumbnail_url = 'http://imgx.' + \
        split_url[2] + '/' + split_url[3] + '/' + size + '/' + split_url[4]
    return thumbnail_url


def upload_photo(photo_file, description, tag, authorization, owner, question, answer):
    # upload photo
    photo_url = storage.obj_upload(photo_file, tag)
    thumbnail_url = get_thumbnail_url(
        photo_url, size='c_fit,w_750')
    # add face to faceset
    person_id_list = faceControl.add_faces(
            method='url', url_or_path=thumbnail_url)
    # save photo and tags
    dbControl.save_photo_and_tag(
        photo_url, description, tag, person_id_list, authorization, owner, question, answer)
    # save info
    photo_info = dbControl.get_photo_info(photo_url, method='url')
    return photo_info

def get_email(request):
    if request.user.is_authenticated():
        email = request.user.email
    else:
        email = None
    return email
