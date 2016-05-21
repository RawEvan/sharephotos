# coding:utf-8
# function of database control
from models import Photo, Tag, Interest, Collect
from users.models import User
import common


def get_photos_of_tag(key, method='tag'):

    """ Get photos which have the tag """

    photo_list = []
    result_photo = []
    # the tag that is person id
    if u'人脸' in key:
        key = key[2:]
    target_tag = Tag.objects.get(tag=key)
    # get photo related to the tag
    result_photo = target_tag.photo_set.all()
    for each_photo in result_photo:
        photo_info = get_photo_info(each_photo, method='obj')
        if photo_info:
            photo_list.append(photo_info)
    return photo_list

def get_owned_photos(email):
    user = User.objects.get(email=email)
    owned_photos = user.photo_set.all()
    for each_photo in owned_photo:
        photo_info = get_photo_info(each_photo, method='obj')
        if photo_info:
            photo_list.append(photo_info)
    return photo_list

def get_related_photos(tag_list):

    """ get photos related to a tag list """

    photo_list = []
    for tag in tag_list:
        photo_list.extend(get_photos_of_tag(tag))
    return photo_list


def get_photo_info(key, method):
    if method == 'p_id':
        photo = Photo.objects.get(id=key)
    elif method == 'url':
        # Original_url is the same as photo_url in database model
        photo = Photo.objects.get(photo_url=key)
    elif method == 'obj':
        photo = key
    else:
        print 'get photo info error'
        photo = ''
    # get tag list and change person tag
    if photo:
        tag_list = []
        got_tag_list = photo.tags.all()
        for each_tag in got_tag_list:
            tag_list.append(each_tag.unified_tag())
        thumbnail_url = common.get_thumbnail_url(photo.photo_url)
        if photo.owner == 'system':
            owner = u'游客'
        else:
            owner = photo.owner
        photo_info = {
            'p_id': photo.id,
            'original_url': photo.photo_url,
            'description': photo.description,
            'owner': owner,
            'thumbnail_url': thumbnail_url,
            "tag_list": tag_list,
            'collected_times': photo.collected_times}
    else:
        # Deal with this later
        photo_info = {}
        print 'get photo info errot'

    return photo_info


def save_photo_and_tag(photo_url, description, tag, person_id_list, permission, owner):
    # TODO:deal with the failure of saving photo or tags
    try:
        photo = add_photo(photo_url, description, permission, owner)
    except:
        return False
    tag_list = tag.split(u'、')
    add_tag(key=photo, tag_list=tag_list,
           method='obj', person_id_list=person_id_list)
    tag_list.extend(person_id_list)
    add_interest(owner, tag_list)
    return True


def add_photo(photo_url, description, permission, owner):
    user = User.objects.get(email=owner)
    photo = Photo(photo_url=photo_url,
                    description=description, permission=permission, owner=user)
    photo.save()
    return photo


def add_tag(key, tag_list, method, person_id_list=[]):
    if method == 'obj':
        photo = key
    elif method == 'p_id':
        photo = Photo.objects.get(id=key)
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
        tagInfo.photo_set.add(photo)
    # person tag
    if person_id_list:
        for tag in person_id_list:
            tagInfo = Tag.objects.get_or_create(tag=tag, is_person=True)[0]
            if tagInfo:
                tagInfo.used_times += 1
            else:
                tagInfo = Tag(tag=tag, is_person=True, used_times=1)
            tagInfo.save()
            tagInfo.photo_set.add(photo)
    return True


def add_interest(owner, tag_list):

    """ Add infomation of interests to the database. """

    user= User.objects.get(email=owner)
    for tag in tag_list:
        tag_obj = Tag.objects.get(tag=tag)
        interest_obj = Interest.objects.get_or_create(user=user, tag=tag_obj)[0]
        if interest_obj:
            interest_obj.degree += 1
        else:
            interest_obj = Interest(user=owner, tag=tag, degree=0)
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
    latest_tag_list = [object.unified_tag() for object in latest_tag_objects]
    return latest_tag_list


def get_interested_photos(email, num_limit=True, num=5):
    """ Get photos that user may Interested in. """
    user = User.objects.get(email=email)
    tags = user.interest_set.all()
    photos = get_related_photos(tags)
    return photos


def get_latest_photos(num_limit=True, num=6):
    """ Get latest photos. """
    photos = []
    if num_limit:
        latest_photos = Photo.objects.all()[:num]
    for p in latest_photos:
        photo = get_photo_info(p, 'obj')
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
    user = User.objects.get(email=email)
    photo = Photo.objects.get(id = photo_id)
    # Update collect
    collect, result = Collect.objects.get_or_create(user=user, photo=photo)
    # If exist, result == False
    if result == False:
        return False
    else:
        collect.save()
        # Update Photo.collected_times
        photo = Photo.objects.get(id=photo_id)
        photo.collected_times += 1
        photo.save()
        tag_list = []
        got_tag_list = photo.tags.all()
        for each_tag in got_tag_list:
            tag_list.append(each_tag.unified_tag())
        # Update Interest
        add_interest(email, tag_list)
        return True


def cancel_collect(email, photo_id):
    """ Cancel collect. """
    user = User.objects.get(email=email)
    photo = Photo.objects.get(id = photo_id)
    try:
        collect = Collect.objects.get(user=user, photo=photo)
        collect.delete()
        photo = Photo.objects.get(id=photo_id)
        photo.collected_times -= 1
        photo.save()
        return True
    except:
        # Deal with it later.
        return False


def get_user_info(email):
    """ Get the infomation of user. """
    info = {}
    photos = []
    user = User.objects.get(email=email)
    interest = user.interest.all()
    collect = user.collect.all()
    for c in collect:
        photo = get_photo_info(c.photo, 'obj')
        if photo:
            photos.append(photo)
    info['id'] = user.id
    info['email'] = user.email
    # i.tag is the tag object, (i.tag).tag is the content.
    info['interest'] = [i.tag.tag for i in interest]
    info['collect'] = photos
    return info


def is_collected(email, photo_id):
    user = User.objects.get(email=email)
    photo = Photo.objects.get(id = photo_id)
    exist_collect = Collect.objects.filter(user=user, photo=photo)
    if exist_collect:
        return True
    else:
        return False


def get_collected_times(photo_id):
    times = Photo.objects.get(id=photo_id).collected_times
    return times
