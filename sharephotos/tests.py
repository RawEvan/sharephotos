from django.test import TestCase
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your tests here.
def EmailTest(request):
    send_mail('Subject_test', 'message', 'sys_sharephotos@sina.com', ['909798432@qq.com'])
    return HttpResponse(u'send success')
