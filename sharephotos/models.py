#coding:utf-8
from django.db import models

# Create your models here.
class tb_photo_info(models.Model):
    store_url = models.TextField(max_length = 1250, default = 'url')
    description = models.TextField(max_length = 300, default = 'no description')
    upload_time = models.DateTimeField(auto_now = True)
    owner = models.TextField(max_length = 1250, default = 'system')
    
    def __unicode__(self):
        return self.description
        
class tb_tag(models.Model):
    tag = models.CharField(max_length = 50, unique = True, blank = False)
    is_face = models.BooleanField(default = False)
    add_time = models.DateTimeField(auto_now = True)
    photo = models.ManyToManyField(tb_photo_info)
    
    def __unicode__(self):
        return self.tag
        
