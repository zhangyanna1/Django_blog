# @Time    : 18-6-5 下午2:19
# @Author  : zhangyanna
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from .views import index,list,base,search,show

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^list/$',list,name='list'),
    url(r'^base/$',base,name='base'),
    url(r'^search/$',search.as_view() , name='search'),
    url(r'^tags/(?P<tid>[0-9]+)/$', list, name='tags'),
    url(r'^category/(?P<cid>[0-9]+)/$', list,name='category'),
    url(r'^xiangqing/(?P<sh>[0-9]+)/$', show, name='show_x'),
    url(r'^show/$',show,name='show'),



]
