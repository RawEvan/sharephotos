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
    url(r'^search$', 'sharephotos.views.search', name = 'search'), #for GET method
    url(r'^photo/(.*?)$', 'sharephotos.views.photo', name = 'photo'),
    url(r'^face_search/$', 'sharephotos.views.face_search', name = 'face_search'),
    url(r'^photo_manage/$', 'sharephotos.views.photo_manage', name = 'photo_manage'),
    url(r'^photo_delete/(\d+)/$', 'sharephotos.views.photo_delete', name = 'photo_delete'),
    url(r'^tag_add/$', 'sharephotos.views.tag_add', name = 'tag_add'),
    url(r'^collect_add/$', 'sharephotos.views.collect_add', name = 'collect_add'),
    url(r'^collect_delete/$', 'sharephotos.views.collect_delete', name = 'collect_delete'),
    url(r'^user_info/$', 'sharephotos.views.user_info', name = 'user_info'),
    url(r'^answer_check/$', 'sharephotos.views.answer_check', name = 'answer_check'),
    url(r'^similarity_update/$', 'sharephotos.views.similarity_update', name = 'similarity_update'),
    #url(r'^tag_delete/$', 'sharephotos.views.tag_delete', name = 'tag_delete'),
]
