# coding:utf-8
# function of database control
from math import sqrt
from models import Photo, Tag, Interest, Collect, Authority, Similarity
from users.models import User
import common


def get_photos_of_tag(key, method='tag'):

    """ Get photos which have the tag """

    photo_list = []
    result_photo = []
    # the tag that is person id
    if u'人脸' in key:
        key = key[2:]
    target_tag = Tag.objects.filter(tag=key)[0]
    if target_tag:
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
    photo_list = []
    if owned_photos:
        for each_photo in owned_photos:
            photo_info = get_photo_info(each_photo, method='obj')
            if photo_info:
                photo_list.append(photo_info)
    return photo_list

def get_related_photos(tag_list):

    """ get photos related to a tag list """

    photo_list = []
    photo_id_list = []
    for tag in tag_list:
        photos = get_photos_of_tag(tag)
        # Get distinct photo info
        photos = [p for p in photos if p['photo_id'] not in photo_id_list]
        photo_id_list.extend([p['photo_id'] for p in photos])
        photo_list.extend(photos)
    return photo_list


def get_photo_info(key, method):
    if method == 'photo_id':
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
            'photo_id': photo.id,
            'original_url': photo.photo_url,
            'description': photo.description,
            'owner': owner,
            'thumbnail_url': thumbnail_url,
            "tag_list": tag_list,
            'collected_times': photo.collected_times,
            'question': photo.question,
            'answer': photo.answer}
    else:
        # Deal with this later
        photo_info = {}
        print 'get photo info errot'

    return photo_info


def save_photo_and_tag(photo_url, description, tag, person_id_list, authorization, owner, question, answer):
    # TODO:deal with the failure of saving photo or tags
    try:
        photo = add_photo(photo_url, description, authorization, owner, question, answer)
    except:
        return False
    tag_list = tag.split(u'、')
    add_tag(key=photo, tag_list=tag_list,
           method='obj', person_id_list=person_id_list)
    tag_list.extend(person_id_list)
    add_interest(owner, tag_list)
    return True


def add_photo(photo_url, description, authorization, owner, question, answer):
    user = User.objects.get(email=owner)
    photo = Photo(photo_url=photo_url,
                    description=description, authorization=authorization, owner=user, question=question, answer=answer)
    photo.save()
    return photo


def add_tag(key, tag_list, method, person_id_list=[]):
    if method == 'obj':
        photo = key
    elif method == 'photo_id':
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


def delete(photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)
        tags = photo.tags.all()
        for tag in tags:
            tag.photo_set.remove(photo)
            if not tag.photo_set.all():
                tag.delete()
        delete_authorization(photo_id)
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
    interest_tags = user.interest_set.all()
    tags = [t.tag.tag for t in interest_tags]
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
    interest = user.interest_set.all()
    collect = user.collect_set.all()
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


def add_authorization(email, photo_id):
    user = User.objects.filter(email=email)[0]
    photo = Photo.objects.filter(id=photo_id)[0]
    authorization = Authority.objects.get_or_create(user=user, photo=photo)


def delete_authorization(photo_id):
    photo = Photo.objects.filter(id=photo_id)[0]
    authorization = Authority.objects.filter(photo=photo)
    for au in authorization:
        au.delete()


def check_answer(photo_id, answer):
    photo = Photo.objects.filter(id=photo_id)[0]
    if answer == photo.answer:
        return True
    else:
        return False

def check_authorization(email, photo_id):
    user = User.objects.filter(email=email)[0]
    photo = Photo.objects.filter(id=photo_id)[0]
    if photo.authorization == 'public':
        result = True
    else:
        authorization = Authority.objects.filter(user=user, photo=photo)
        if authorization.exists():
            result = True
        else:
            result = False
    return result

def get_question(photo_id):
    photo = Photo.objects.filter(id=photo_id)[0]
    if photo:
        question = photo.question
    else:
        question = ''
    return question


def similarity_update():
    import pdb
    pdb.set_trace()
    Similarity.objects.all().delete()
    tags = Tag.objects.all().order_by('id')
    for tag in tags:
        photos = tag.photo_set.all()
        for i in range(len(photos)):
            for j in range(i+1, len(photos)):
                add_similarity(photos[i], photos[j])
                add_similarity(photos[j], photos[i])


def add_similarity(photo_1, photo_2):
    new_similarity = Similarity.objects.get_or_create(
            photo_1=photo_1, photo_2=photo_2)[0]
    new_similarity.similar_count += 1
    new_similarity.similar_degree = count_similarity(photo_1, photo_2,
            new_similarity.similar_count)
    print 'similarity:'
    print new_similarity.similar_count
    print new_similarity.similar_degree
    new_similarity.save()


def count_similarity(photo_1, photo_2, similar_count):
    count_1 = photo_1.tags.count()
    count_2 = photo_2.tags.count()
    new_degree = similar_count/sqrt(count_1 * count_2)
    return new_degree


def get_recommend_photos(email):
    import pdb
    pdb.set_trace()
    # Get condidate photos.
    photos = get_condidate_photos(email)
    # Pick up photos that most interested in.
    recommend_photos = most_interested(email, photos)
    photos = []
    for photo in recommend_photos:
        photos.append(get_photo_info(photo, 'obj'))
    return photos


def get_condidate_photos(email):
    user = User.objects.get(email=email)
    photos = user.photo_set.all()
    collects = user.collect_set.all()
    collect_photos = [c.photo for p in collects]
    photos.extend(collect_photos)
    condidate = {}
    for photo in photos:
        # Get similar photos of each photo.
        similarities = photo.photo_1.all().order_by('similar_degree')[:10]
        for s in similarities:
            photo_2 = s.photo_2
            #check if the photo in condidate, collect_photos or owned_photos
            if photo_2 not in condidate and photo_2 not in photos:
                condidate[photo_2.id] = photo_2
    return condidate.values()


def most_interested(email, photos):
    user = User.objects.get(email=email)
    interests = user.interest_set.all()
    collects = user.collect_set.all()
    collect_photos = [c.photo for p in collects]
    owned_photos = user.photo_set.all()
    interest_tags = [i.tag for i in interests]
    marks = {}
    for photo in photos:
        photo_mark = 0
        tags = photo.tags.all()
        # Count the sum mark of each tag.
        for tag in tags:
            if tag in interest_tags:
                photo_mark += Interest.objects.get(user=user, tag=tag).degree
        marks[photo] = photo_mark
    # Get sorted tuple of marks.
    sorted_marks = sorted(marks.items(), key=lambda m: m[1])
    sorted_photos = [m[0] for m in sorted_marks][-10:]
    return sorted_photos
