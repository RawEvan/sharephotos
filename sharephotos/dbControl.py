# coding:utf-8
# function of database control
from models import tb_photo_info, tb_tag
import common
import pdb

def getRelatedPhotos(key, method = 'tag'):
    #pdb.set_trace()
    try:
        if method == 'tag':
            targetTag = tb_tag.objects.get(tag = key)
            result_photo = targetTag.photo.all()    # get photo related to the tag 
        elif method == 'owner':
            result_photo = tb_photo_info.objects.filter(owner = key)
    except:
        #targetTag = tb_tag.objects.get(tag = u'没有找到图片')
        photo_list = []
        return photo_list

    photo_list = []
    for each_photo in result_photo:
        original_url = each_photo.store_url
        thumbnail_url = common.get_thumbnail_url(original_url)
        photo_dict = {
        'p_id': each_photo.id,
        'original_url': original_url,
        'thumbnail_url': thumbnail_url, 
        'description': each_photo.description, 
        "tags_list": [each_tag.tag for each_tag in each_photo.tb_tag_set.all()]}
        photo_list.append(photo_dict)
    return photo_list
    
def savePhotoAndTag(storeUrl, description, tag_list, face_id_list):
    photoInfo = tb_photo_info(store_url = storeUrl, description = description)
    photoInfo.save()
    for tag in tag_list:
        tagInfo = tb_tag.objects.get_or_create(tag = tag)[0]
        tagInfo.save()
        tagInfo.photo.add(photoInfo) # add relation between tag and photo
    if face_id_list:   
        for tag in face_id_list:
            tagInfo = tb_tag.objects.get_or_create(tag = tag, is_face = True)[0]
            tagInfo.save()
            tagInfo.photo.add(photoInfo) # add relation between tag and photo
        
def getPhotoInfo(method, search_word):
    '''try:
        photoObj = tb_photo_info.objects.get(store_url = photo_url)
    except:
        no_photo = tb_tag.objects.get(tag = u'没有找到图片')
        photoObj = no_photo.photo.all()[0]'''
    if method == 'p_id':
        p_id = search_word
        try:
            photoObj = tb_photo_info.objects.get(id = p_id)
        except:
            no_photo = tb_tag.objects.get(tag = u'没有找到图片')
            photoObj = no_photo.photo.all()[0]
    elif method == 'url':
        photo_url = search_word
        try:
            photoObj = tb_photo_info.objects.get(store_url = photo_url)
        except:
            no_photo = tb_tag.objects.get(tag = u'没有找到图片')
            photoObj = no_photo.photo.all()[0]
    else:
        no_photo = tb_tag.objects.get(tag = u'没有找到图片')
        photoObj = no_photo.photo.all()[0]
    tags_list = []
    got_tags_list = photoObj.tb_tag_set.all()
    for each_tag in got_tags_list:
        if each_tag.is_face:
            each_tag = u'人脸：' + each_tag[:6]
        tags_list.append(each_tag)
    photo_info = {
    'description': photoObj.description, 
    'photo_url': photoObj.store_url,
    "tags_list": tags_list}
    return photo_info

def delete(p_id):
    photo = tb_photo_info.objects.get(id = p_id)
    photo.delete()
