# coding:utf-8
# some common function

def get_thumbnail_url(original_url, size = 'w_250,h_150'):
        split_url = original_url.split('/')
        thumbnail_url = 'http://imgx.' + split_url[2] + '/' +split_url[3] + '/' + size + '/' + split_url[4]
        return thumbnail_url

def getEmail(request):
    try:
        Email = request.user.email
    except:
        Email = False
    return Email
