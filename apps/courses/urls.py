# _*_ encoding:utf-8 _*_
__author__ = 'jiangxiaoyan'
__data__ = ' 10:05'

from django.conf.urls import url
from views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentsView,VideoPlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    #添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]