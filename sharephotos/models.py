# coding:utf-8
from django.db import models


class tb_tag(models.Model):
    """ Model of tag. """
    tag = models.CharField(max_length=50, unique=True, blank=False)
    is_face = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now=True)
    used_times = models.IntegerField(default=0)

    def unifiedTag(self):
        if self.is_face:
            return u'人脸' + self.tag
        else:
            return self.tag

    def __unicode__(self):
        return self.tag


class tb_photo(models.Model):
    """ Model of photo. """
    store_url = models.TextField(max_length=1250, default='url')
    description = models.TextField(max_length=300, default='no description')
    upload_time = models.DateTimeField(auto_now=True)
    owner = models.TextField(max_length=1250, default='system')
    collected_times = models.IntegerField(default=0)
    # permission:
    # private: only friend can see the photo;
    # public: all people can see the photo.
    permission = models.CharField(max_length=20, default='private')
    tags = models.ManyToManyField(tb_tag)

    def __unicode__(self):
        return self.description
