# _*_ encoding:utf-8 _*_
"""guetonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
#from django.contrib import admin
from django.views.static import serve
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView,IndexView
from organization.views import OrgView
from guetonline.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',IndexView.as_view(),name= 'index'),
    url(r'^login/$',LoginView.as_view(),name= 'login'),
    url(r'^logout/$',LogoutView.as_view(),name= 'logout'),
    url(r'^register/$',RegisterView.as_view(),name= 'register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name= 'user_active'),
    url(r'^forget/$',ForgetPwdView.as_view(),name= 'forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name= 'reset_pwd'),
    url(r'^modifypwd/$',ModifyPwdView.as_view(),name= 'modify_pwd'),
    #配置课程机构的URL
    url(r'^org/', include('organization.urls',namespace='org')),
    #配置上传按访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    #配置课程的URL
    url(r'^course/', include('courses.urls',namespace='course')),
    #配置课程的URL
    url(r'^teacher/', include('courses.urls',namespace='teacher')),
    #配置用户个人中心的URL
    url(r'^users/', include('users.url',namespace='users')),
]
