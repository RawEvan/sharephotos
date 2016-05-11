# coding:utf-8
# function of database control
from models import Photo, Tag, Interest, Collect
import users
import common
import re


def getPhotosOfTag(key, method='tag'):

    """ Get photos which have the tag """

    photo_list = []
    result_photo = []
    try:
        if method == 'tag':
            # the tag that is person id
            reg = u'人脸' + r'\d+?'
            if re.search(reg, key):
                key = key[2:]
            targetTag = Tag.objects.get(tag=key)
            # get photo related to the tag
            result_photo = targetTag.photo_set.all()
        elif method == 'owner':
            result_photo = Photo.objects.filter(owner=key)
    except:
        pass
    for each_photo in result_photo:
        photo_info = getPhotoInfo(each_photo, method='obj')
        if photo_info:
            photo_list.append(photo_info)
    return photo_list


def getRelatedPhotos(tag_list):

    """ get photos related to a tag list """

    photo_list = []
    for tag in tag_list:
        photo_list.extend(getPhotosOfTag(tag))
    return photo_list


def getPhotoInfo(key, method):
    if method == 'p_id':
        photoObj = Photo.objects.get(id=key)
    elif method == 'url':
        # Original_url is the same as photo_url in database model
        photoObj = Photo.objects.get(photo_url=key)
    elif method == 'obj':
        photoObj = key
    else:
        print 'get photo info error'
        photoObj = ''
    # get tag list and change person tag
    if photoObj:
        tag_list = []
        got_tag_list = photoObj.tags.all()
        for each_tag in got_tag_list:
            tag_list.append(each_tag.unifiedTag())
        thumbnail_url = common.get_thumbnail_url(photoObj.photo_url)
        if photoObj.owner == 'system':
            owner = u'游客'
        else:
            owner = photoObj.owner
        photo_info = {
            'p_id': photoObj.id,
            'original_url': photoObj.photo_url,
            'description': photoObj.description,
            'owner': owner,
            'thumbnail_url': thumbnail_url,
            "tag_list": tag_list,
            'collected_times': photoObj.collected_times}
    else:
        # Deal with this later
        photo_info = {}
        print 'get photo info errot'

    return photo_info


def savePhotoAndTag(photo_url, description, tag, person_id_list, permission, owner):
    # TODO:deal with the failure of saving photo or tags
    try:
        photoObj = addPhoto(photo_url, description, permission, owner)
    except:
        return False
    tag_list = tag.split(u'、')
    addTag(key=photoObj, tag_list=tag_list,
           method='obj', person_id_list=person_id_list)
    tag_list.extend(person_id_list)
    add_interest(owner, tag_list)
    return True


def addPhoto(photo_url, description, permission, owner):
    photoObj = Photo(photo_url=photo_url,
                    description=description, permission=permission, owner=owner)
    photoObj.save()
    return photoObj


def addTag(key, tag_list, method, person_id_list=[]):
    if method == 'obj':
        photoObj = key
    elif method == 'p_id':
        photoObj = Photo.objects.get(id=key)
    else:
        return False
    # add tag and relation between tag and photo
    # nomal tag
    for tag in tag_list:
        tagInfo = Tag.objects.get_or_create(tag=tag)[0]
        if tagInfo:
            tagInfo.used_times += 1
        else:
            tagInfo = Tag(tag=tag, is_person=True, used_times=1)
        tagInfo.save()
        tagInfo.photo_set.add(photoObj)
    # person tag
    if person_id_list:
        for tag in person_id_list:
            tagInfo = Tag.objects.get_or_create(tag=tag, is_person=True)[0]
            if tagInfo:
                tagInfo.used_times += 1
            else:
                tagInfo = Tag(tag=tag, is_person=True, used_times=1)
            tagInfo.save()
            tagInfo.photo_set.add(photoObj)
    return True


def add_interest(owner, tag_list):

    """ Add infomation of interests to the database. """

    for tag in tag_list:
        interest_obj = Interest.objects.get_or_create(email=owner, interested_tag=tag)[0]
        if interest_obj:
            interest_obj.degree += 1
        else:
            interest_obj = Interest(email=owner, interested_tag=tag, degree=0)
        interest_obj.save()


def delete(p_id):
    try:
        photo = Photo.objects.get(id=p_id)
        tags = photo.tags.all()
        for tag in tags:
            tag.photo_set.remove(photo)
            if not tag.photo_set.all():
                tag.delete()
        photo.delete()
        return True
    except:
        return False


def get_latest_tags(num=5):
    """ Get the latest 5 tags. """
    latest_tag_objects = Tag.objects.all().order_by('-id')[:5]
    latest_tag_list = [object.unifiedTag() for object in latest_tag_objects]
    return latest_tag_list


def get_interest_tags(email, num_limit=True, num=5):
    """ Get the tags that user interested in. """
    interests = Interest.objects.filter(email=email).order_by('degree')
    tags = []
    if num_limit and len(interests) > num:
        interests = interests[:num]
    for i in interests:
        tags.append(i.interested_tag)
    return tags


def get_interested_photos(email, num_limit=True, num=5):
    """ Get photos that user may Interested in. """
    tags = get_interest_tags(email)
    photos = getRelatedPhotos(tags)
    return photos


def get_latest_photos(num_limit=True, num=6):
    """ Get latest photos. """
    photos = []
    if num_limit:
        latest_photos = Photo.objects.all()[:num]
    for p in latest_photos:
        photo = getPhotoInfo(p, 'obj')
        if photo:
            photos.append(photo)
    return photos


def add_collect(email, photo_id):
    """
    This function makes 3 changes:
    --Update Collect
    --Update Interest
    --Add Photo.collected_times
    """
    # Update collect
    collect, result = Collect.objects.get_or_create(email=email, photo_id=photo_id)
    # If exist, result == False
    if result == False:
        return False
    else:
        collect.save()
        # Update Photo.collected_times
        photoObj = Photo.objects.get(id=photo_id)
        photoObj.collected_times += 1
        photoObj.save()
        tag_list = []
        got_tag_list = photoObj.tags.all()
        for each_tag in got_tag_list:
            tag_list.append(each_tag.unifiedTag())
        # Update Interest
        add_interest(email, tag_list)
        return True


def cancel_collect(email, photo_id):
    """ Cancel collect. """
    try:
        collect = Collect.objects.get(email=email, photo_id=photo_id)
        collect.delete()
        photoObj = Photo.objects.get(id=photo_id)
        photoObj.collected_times -= 1
        photoObj.save()
        return True
    except:
        # Deal with it later.
        return False


def get_user_info(email):
    """ Get the infomation of user. """
    info = {}
    photos = []
    user = users.models.User.objects.get(email=email)
    interest = Interest.objects.filter(email=email)
    collect = Collect.objects.filter(email=email)
    for c in collect:
        photo = getPhotoInfo(c.photo_id, 'p_id')
        if photo:
            photos.append(photo)
    info['id'] = user.id
    info['email'] = user.email
    info['interest'] = [i.interested_tag for i in interest]
    info['collect'] = photos
    return info


def is_collected(email, photo_id):
    exist_collect = Collect.objects.filter(email=email, photo_id=photo_id)
    if exist_collect:
        return True
    else:
        return False


def get_collected_times(photo_id):
    times = Photo.objects.get(id=photo_id).collected_times
    return times
