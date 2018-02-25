# _*_ encoding:utf-8 _*_
__author__ = 'jiangxiaoyan'
__data__ = ' 14:31'

from django.conf.urls import url
from .views import UserInfoView, UploadImageView,UpdatePwdView,MyCourseView,MyFavOrgView,MyFavTeacherView,\
    MyFavCourseView,MyMessageView


urlpatterns = [
    #用户信息
    url(r'^info/$',UserInfoView.as_view(),name= 'user_info'),
    # 用户上传头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='my_course'),
    # 我的收藏机构
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我的收藏教师
    url(r'^myfavteacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我的收藏课程
    url(r'^myfavcourse/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='my_message'),
]