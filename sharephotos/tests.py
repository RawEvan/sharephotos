# coding:utf-8
from django.test import TestCase
from django.http import HttpResponse
from django.core.mail import send_mail
from models import Photo, Tag, Interest, Collect
from users.models import User
import dbControl
import faceControl
import time


class DBTestCase(TestCase):

    """ Test for functions of database controling. """

    def setUp(self):
        test_user = User(email='test@test.com')
        test_user.save()

    def test_add_interest(self):
        tag_list = ['test_tag_1', 'test_tag_2']
        got_tag_list = []
        test_owner = 'test@test.com'
        dbControl.add_interest(test_owner, tag_list)
        interest_obj = Interest.objects.get(email=test_owner, interested_tag=tag_list[0])
        self.assertEqual(interest_obj.degree, 1)

    def test_add_collect(self):
        import pdb
        pdb.set_trace()
        email = 'test@test.com'
        photo_url = 'test_url'
        tag = u'tag1、tag2'
        dbControl.save_photo_and_tag(photo_url=photo_url, description='no',
                tag=tag, person_id_list=[], permission='public', owner=email)
        photo_id= Photo.objects.get(photo_url=photo_url).id
        dbControl.add_collect(email, photo_id)
        collected_times = Photo.objects.get(id=photo_id).collected_times

        self.assertTrue(Collect.objects.get(
                email=email, photo_id=photo_id))
        self.assertEqual(collected_times, 1)
        self.assertTrue(Interest.objects.get(email=email, interested_tag='tag2'))

    def test_cancel_collect(self):
        email = 'test@test.com'
        photo_url = 'test_url'
        tag = u'tag1、tag2'
        dbControl.save_photo_and_tag(photo_url=photo_url, description='no',
                tag=tag, person_id_list=[], permission='public', owner=email)
        photo_id= Photo.objects.get(photo_url=photo_url).id
        dbControl.add_collect(email, photo_id)
        collected_times = Photo.objects.get(id=photo_id).collected_times
        self.assertEqual(collected_times, 1)

        dbControl.cancel_collect(email=email, photo_id=photo_id)
        collected_times = Photo.objects.get(id=photo_id).collected_times
        self.assertEqual(collected_times, 0)


class UploadTestCase(TestCase):

    """ TestCase for view: upload. """

    def test_upload(self):
        pass


class FaceTestCase(TestCase):

    """ TestCase for faceControl. """

    def test_add_face(self):
        got_person_list = faceControl.add_faces(
            'url', 'http://cdn.sinacloud.net/sharephotos/%E5%A5%A5%E5%B7%B4%E9%A9%AC%E3%80%81%E7%B1%B3%E6%AD%87_Mon_Apr_18_00%3A16%3A01_2016.jpg')
        # It's a photo with two persons, so the length is 2.
        self.assertEqual(len(got_person_list), 2)


def EmailTest(request):
    """ Test the function of sending Email. It's not a nomal testcase. """

    message = '%s, Email from sharephotos.sinaapp.com' % time.ctime()
    send_mail('Subject_test', message,
              'sys_sharephotos@sina.com', ['liaiwen_mail@163.com'])
    return HttpResponse(u'send success')
