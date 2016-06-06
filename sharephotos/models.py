# coding:utf-8
from django.db import models
from users.models import User


class Tag(models.Model):
    """ Model of tag. """
    tag = models.CharField(max_length=50, unique=True, blank=False)
    is_person = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now=True)
    used_times = models.IntegerField(default=1)

    def unified_tag(self):
        if self.is_person:
            return u'人脸' + self.tag
        else:
            return self.tag

    def __unicode__(self):
        return self.tag


class Photo(models.Model):
    """ Model of photo. """
    photo_url = models.TextField(max_length=1250, default='url')
    description = models.TextField(max_length=300, default='no description')
    upload_time = models.DateTimeField(auto_now=True)
    collected_times = models.IntegerField(default=0)
    # authorization:
    # private: only friend can see the photo;
    # public: all people can see the photo.
    authorization = models.CharField(max_length=20, default='public')
    question = models.CharField(max_length=20, default='')
    answer= models.CharField(max_length=20, default='')


    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.description + 'id:' + str(self.id)


class Interest(models.Model):
    """ Model of User's intersts. """
    # The times that the user interested in the tag
    degree = models.IntegerField(default=0)

    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = ('user', 'tag')
        
class Collect(models.Model):
    """ Model of User's collect. """
    collect_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)

    class Meta:
        unique_together = ('user', 'photo')

class Authority(models.Model):
    """ Model of authority for viewing the photo. """
    add_time = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)

    class Meta:
        unique_together = ('user', 'photo')


class Similarity(models.Model):
    """ Model of similarity between two photos. """
    similar_count = models.IntegerField(default = 0)
    similar_degree = models.FloatField(default = 0.0)

    photo_1 = models.ForeignKey(Photo, related_name='photo_1')
    photo_2 = models.ForeignKey(Photo, related_name='photo_2')

    class Meta:
        unique_together = ('photo_1', 'photo_2')

