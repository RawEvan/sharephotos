# coding:utf-8
# function for cookies
import dbControl
import pdb

def latest_tags_list(request, response):
    if 'latest_tags_list' is request.COOKIES:
        latest_tags_list = request.COOKIES['latest_tags_list']
    else:
        latest_tags_list = dbControl.get_latest_tags()
        response.set_cookie('latest_tags_list', latest_tags_list)
        pdb.set_trace()
    return (latest_tags_list, response)

