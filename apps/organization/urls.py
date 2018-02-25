# _*_ encoding:utf-8 _*_
__author__ = 'jiangxiaoyan'
__data__ = ' 20:40'

from django.conf.urls import url,include
from views import OrgView,AddUserAskView,OgrHomeView,OgrCourseView,OgrDescView,OgrTeacherView,\
    AddFavView,TeacherListView,TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OgrHomeView.as_view(), name='org_home'),
    url(r'^cource/(?P<org_id>\d+)/$', OgrCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OgrDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OgrTeacherView.as_view(), name='org_teacher'),
    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    #教师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]