from django.test import TestCase
from django.http import HttpResponse
from django.core.mail import send_mail
from models import tb_photo, tb_tag
import dbControl
import time

'''
def EmailTest(request):
    message = '%s, Email from sharephotos.sinaapp.com' % time.ctime()
    send_mail('Subject_test', message, 'sys_sharephotos@sina.com', ['909798432@qq.com'])
    return HttpResponse(u'send success')
'''

class dbTestCase(TestCase):
    def setUp(self):
        self.url = 'http://testStoreUrl.jpg'
        self.description = 'testDescription'
        self.tagList = ['tag1', 'tag2']
        self.faceIdList = ['faceId1', 'faceId2']
        self.allTagList = self.tagList + self.faceIdList
        self.owner = 'testOwner'
        dbControl.savePhotoAndTag(self.url, self.description, self.tagList, self.faceIdList, self.owner)
    def testSavePhotoAndTag(self):
        photoInfo = tb_photo_info.objects.get()
        # get tag list
        tagObjList= photoInfo.tags.all()
        gotTagList = []
        for each_tag in tagObjList:
            gotTagList.append(each_tag.tag)
        gotInfoList = [photoInfo.store_url,
                photoInfo.description,
                gotTagList,
                photoInfo.owner]
        testInfoList = [self.url,
                self.description,
                self.allTagList,
                self.owner]
        self.assertEqual(gotInfoList, testInfoList)
