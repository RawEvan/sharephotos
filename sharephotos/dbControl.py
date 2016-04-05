# coding:utf-8
# function of database control
from models import tb_photo_info, tb_tag
import common
import pdb
import re

def getRelatedPhotos(key, method = 'tag'):
    photo_list = []
    result_photo = []
    try:
        if method == 'tag':
            #the tag that is face id
            reg = u'人脸' + r'\d+?'
            if re.search(reg, key):
                key = key[2:]
            targetTag = tb_tag.objects.get(tag = key)
            result_photo = targetTag.photo.all()    # get photo related to the tag 
        elif method == 'owner':
            result_photo = tb_photo_info.objects.filter(owner = key)
    except:
        pass
    for each_photo in result_photo:
        original_url = each_photo.store_url
        photo_info = getPhotoInfo(each_photo, method = 'obj')
        photo_list.append(photo_info)
    return photo_list
    
def getPhotoInfo(key, method):
    if method == 'p_id':
        try:
            photoObj = tb_photo_info.objects.get(id = key)
        except:
            pass
    elif method == 'url':
        try:
            #original_url is the same as store_url in database model
            photoObj = tb_photo_info.objects.get(store_url = key)
        except:
            pass
    elif method == 'obj':
        photoObj = key
    else:
        pass
    #get tag list and change face tag
    tag_list = []
    try:
        got_tag_list = photoObj.tb_tag_set.all()
        for each_tag in got_tag_list:
            tag_list.append(each_tag.unifiedTag())
    except:
        pass

    thumbnail_url = common.get_thumbnail_url(photoObj.store_url)
    if  photoObj.owner == 'system':
        owner = u'游客'
    else:
        owner = photoObj.owner
    photo_info = {
        'p_id': photoObj.id,
        'original_url': photoObj.store_url,
        'description': photoObj.description, 
        'owner': owner,
        'thumbnail_url': thumbnail_url, 
        "tag_list": tag_list}

    return photo_info

def savePhotoAndTag(storeUrl, description, tag_list, face_id_list, owner):
    #TODO:deal with the failure of saving photo or tags
    try:
        photoObj = addPhoto(storeUrl, description, owner)
    except:
        return False
    addTag(key = photoObj, tag_list = tag_list, method = 'obj', face_id_list = face_id_list)
    return True
        
def addPhoto(storeUrl, description, owner):
    photoObj = tb_photo_info(store_url = storeUrl, description = description, owner = owner)
    photoObj.save()
    return photoObj

def addTag(key, tag_list, method, face_id_list = []):
    if method == 'obj':
        photoObj = key
    elif method == 'p_id':
        photoObj = tb_photo_info.objects.get(id = key)
    else:
        return False
    # add tag and relation between tag and photo
    # nomal tag
    for tag in tag_list:
        tagInfo = tb_tag.objects.get_or_create(tag = tag)[0]
        tagInfo.save()
        tagInfo.photo.add(photoObj) 
    # face tag
    if face_id_list:   
        for tag in face_id_list:
            tagInfo = tb_tag.objects.get_or_create(tag = tag, is_face = True)[0]
            tagInfo.save()
            tagInfo.photo.add(photoObj) 
    return True

def delete(p_id):
    try:
        import pdb
        pdb.set_trace()
        photo = tb_photo_info.objects.get(id = p_id)
        tags = photo.tb_tag_set.all()
        for tag in tags:
            tag.photo.remove(photo)
            if not tag.photo.all():
                tag.delete()
        photo.delete()
        return True
    except:
        return False

def get_latest_tags(num = 5):
    latest_tag_objects = tb_tag.objects.all().order_by('-id')[:5]
    latest_tag_list = [object.unifiedTag() for object in latest_tag_objects]
    return latest_tag_list

def tagOfPhotoExist(tag, p_id):
#    photoObj = tb_photo_info.objects.get(id = key)
#    if photoObj.tb_tag_set.get(tag = tag):
#        return True
#    else:
#        return False
    return True
