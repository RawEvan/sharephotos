"""graduation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import sharephotos.views
import users

#admin.autodiscover()#in django1.7.x

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('users.urls')),
    url(r'^$', 'sharephotos.views.homepage', name = 'homepage'),
    url(r'^upload/$', 'sharephotos.views.upload', name = 'upload'),
    url(r'^tag/(.*?)/$', 'sharephotos.views.tag', name = 'tag'), #for url method(using url derectly)
    url(r'^tag$', 'sharephotos.views.formTag', name = 'formTag'), #for GET method
    url(r'^photo/$', 'sharephotos.views.photo', name = 'photo'),
    url(r'^face/$', 'sharephotos.views.face', name = 'face'),
    url(r'^photo_manage/$', 'sharephotos.views.photoManage', name = 'photoManage'),
    url(r'^delete/(\d+)/$', 'sharephotos.views.delete', name = 'delete'),
    url(r'^addTag/$', 'sharephotos.views.addTag', name = 'addTag'),
    url(r'^add_collect/$', 'sharephotos.views.add_collect', name = 'add_collect'),
    url(r'^cancel_collect/$', 'sharephotos.views.cancel_collect', name = 'cancel_collect'),
    url(r'^user_info/$', 'sharephotos.views.user_info', name = 'user_info'),
    #url(r'^deleteTag/$', 'sharephotos.views.deleteTag', name = 'deleteTag'),
]
