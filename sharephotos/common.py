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


def uploadPhoto(photo_file, description, tag, permission, owner):
    # upload photo
    photo_url = storage.objUpload(photo_file, tag)
    thumbnail_url = get_thumbnail_url(
        photo_url, size='c_fit,w_750')
    # add face to faceset
    person_id_list = faceControl.add_faces(
            method='url', url_or_path=thumbnail_url)
    # save photo and tags
    dbControl.savePhotoAndTag(
        photo_url, description, tag, person_id_list, permission, owner)
    # save info
    photo_info = dbControl.getPhotoInfo(photo_url, method='url')
    return photo_info

def get_email(request):
    try:
        Email = request.user.email
    except:
        print 'no owner'
        Email = '2012406855@qq.com'
    return Email
