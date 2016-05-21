# coding:utf-8
import urllib2
from sinastorage.bucket import SCSBucket, ACL
import sinastorage
import time
import ConfigParser

cp = ConfigParser.ConfigParser()
cp.read('project.conf')
API_KEY = cp.get('storage', 'API_KEY')
API_SECRET = cp.get('storage', 'API_SECRET')
acl = {}
acl[ACL.ACL_GROUP_ANONYMOUSE] = [ACL.ACL_READ]
acl[ACL.ACL_GROUP_CANONICAL] = [
    ACL.ACL_READ, ACL.ACL_READ_ACP, ACL.ACL_WRITE_ACP]


def url_upload(imgSrc='http://www.w3school.com.cn/i/site_photoref.jpg'):

    """ Upload photo by url. """

    sinastorage.setDefaultAppInfo(API_KEY, API_SECRET)
    s = SCSBucket('sharephotos')
    data = urllib2.urlopen(imgSrc).read()
    path = imgSrc.split('/')[2] + '/%s__' % time.ctime()
    # if '/' in file name there will be problems
    filename = path + imgSrc.replace('/', '_')
    scs_response = s.put(filename, data)
    s.update_acl(filename, acl)
    url = s.make_url(filename)   # get url of image in the storage
    return url


def obj_upload(data, fileTag):

    """ Upload photo by object. """

    sinastorage.setDefaultAppInfo(API_KEY, API_SECRET)
    s = SCSBucket('sharephotos')
    path = time.ctime().replace(' ', '_')
    # if '/' in file name there will be problems
    filename = fileTag[:6] + '_' + path + '.jpg'  # use jpg temporary
    scs_response = s.put(filename, data)
    s.update_acl(filename, acl)
    url = s.make_url(filename)   # get url of image in the storage
    return url
