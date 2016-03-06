from django.test import TestCase
from django.http import HttpResponse
from django.core.mail import send_mail
import time
# Create your tests here.
def EmailTest(request):
    message = '%s, Email from sharephotos.sinaapp.com' % time.ctime()
    send_mail('Subject_test', message, 'sys_sharephotos@sina.com', ['909798432@qq.com'])
    return HttpResponse(u'send success')
