# coding:utf-8
from django.db import models


class Tag(models.Model):
    """ Model of tag. """
    tag = models.CharField(max_length=50, unique=True, blank=False)
    is_person = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now=True)
    used_times = models.IntegerField(default=1)

    def unifiedTag(self):
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
    owner = models.TextField(max_length=1250, default='system')
    collected_times = models.IntegerField(default=0)
    # permission:
    # private: only friend can see the photo;
    # public: all people can see the photo.
    permission = models.CharField(max_length=20, default='private')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.description


class Interest(models.Model):
    """Model of User's intersts. """
    email = models.EmailField(max_length=255)
    interested_tag = models.CharField(max_length=50, blank=False)
    # The times that the user interested in the tag
    degree = models.IntegerField(default=0)

    class Meta:
        unique_together = ('email', 'interested_tag')
        
class Collect(models.Model):
    """Model of User's collect. """
    email = models.EmailField(max_length=255)
    photo_id = models.IntegerField(default=0)
    collect_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('email', 'photo_id')
