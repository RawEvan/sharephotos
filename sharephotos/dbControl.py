# coding:utf-8
# function of database control
from models import tb_photo_info, tb_tag
import pdb

def getRelatedPhotos(search_word):
    #pdb.set_trace()
    try:
        targetTag = tb_tag.objects.get(tag = search_word)
    except:
        targetTag = tb_tag.objects.get(tag = u'没有找到图片')
    result_photo = targetTag.photo.all()    # get photo related to the tag 
    photo_list = []
    for each_photo in result_photo:
        original_url = each_photo.store_url
        split_url = original_url.split('/')
        size = 'w_200,h_150'
        thumbnail_url = 'http://imgx.' + split_url[2] + '/' +split_url[3] + '/' + size + '/' + split_url[4]
        photo_dict = {'original_url': original_url, 'thumbnail_url': thumbnail_url, 
        'description': each_photo.description}
        photo_list.append(photo_dict)
    return photo_list
    
def savePhotoAndTag(storeUrl, description, tag):
    photoInfo = tb_photo_info(store_url = storeUrl, description = description)
    photoInfo.save()
    tagInfo = tb_tag.objects.get_or_create(tag = tag)[0]
    tagInfo.save()
    tagInfo.photo.add(photoInfo) # add relation between tag and photo