import urllib2
from sinastorage.bucket import SCSBucket
import sinastorage
import time
def upload(imgSrc = 'http://www.w3school.com.cn/i/site_photoref.jpg'):
    sinastorage.setDefaultAppInfo('1cjfyo5kQPdnsI3cUc6W',
                                  'a3c139370a3509f269331930515729747573aa10')
    s = SCSBucket('sharephotos')
    data = urllib2.urlopen(imgSrc).read()
    path = imgSrc.split('/')[2] + '/%s__' % time.ctime()
    # if '/' in file name there will be problems
    filename = path + imgSrc.replace('/', '@')
    scsResponse = s.put(filename, data)
    stUrl = s.make_url(filename)   # get url of image in the storage
    return stUrl
