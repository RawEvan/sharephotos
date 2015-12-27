#coding:utf-8
import urllib2
from sinastorage.bucket import SCSBucket, ACL
import sinastorage
import time

acl = {}
acl[ACL.ACL_GROUP_ANONYMOUSE] = [ACL.ACL_READ]
acl[ACL.ACL_GROUP_CANONICAL] = [ACL.ACL_READ, ACL.ACL_READ_ACP,ACL.ACL_WRITE_ACP]

def urlUpload(imgSrc = 'http://www.w3school.com.cn/i/site_photoref.jpg'):
    sinastorage.setDefaultAppInfo('1cjfyo5kQPdnsI3cUc6W',
                                  'a3c139370a3509f269331930515729747573aa10')
    s = SCSBucket('sharephotos')
    data = urllib2.urlopen(imgSrc).read()
    path = imgSrc.split('/')[2] + '/%s__' % time.ctime()
    # if '/' in file name there will be problems
    filename = path + imgSrc.replace('/', '_')
    scsResponse = s.put(filename, data)
    s.update_acl(filename, acl)
    stUrl = s.make_url(filename)   # get url of image in the storage
    return stUrl

def objUpload(data, tag):
    sinastorage.setDefaultAppInfo('1cjfyo5kQPdnsI3cUc6W',
                                  'a3c139370a3509f269331930515729747573aa10')
    s = SCSBucket('sharephotos')
    path = time.ctime()
    # if '/' in file name there will be problems
    filename = tag + '_' + path + '.jpg' # use jpg temporary
    scsResponse = s.put(filename, data)
    s.update_acl(filename, acl)
    stUrl = s.make_url(filename)   # get url of image in the storage
    return stUrl