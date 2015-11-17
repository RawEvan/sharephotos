import urllib2
from sinastorage.bucket import SCSBucket
import sinastorage
import time
def upload():
    sinastorage.setDefaultAppInfo('1cjfyo5kQPdnsI3cUc6W',
                                  'a3c139370a3509f269331930515729747573aa10')
    s = SCSBucket('sharephotos')

    imgSrc = 'http://img0.bdstatic.com/img/image/shouye/bizhi1109.jpg'
    data = urllib2.urlopen(imgSrc).read()
    path = imgSrc.split('/')[2] + '/%s__' % time.ctime()
    # if '/' in file name there will be problems
    filename = path + imgSrc.replace('/', '@')
    scsResponse = s.put(filename, data)
    
    stUrl = s.make_url_authed(filename)   # get url of image in the storage

    return stUrl
