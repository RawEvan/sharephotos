# coding:utf-8
# some common function

def get_thumbnail_url(original_url):
        split_url = original_url.split('/')
        size = 'w_300,h_180'
        thumbnail_url = 'http://imgx.' + split_url[2] + '/' +split_url[3] + '/' + size + '/' + split_url[4]
        return thumbnail_url