# _*_ encoding:utf-8 _*_
__author__ = 'jiangxiaoyan'
__data__ = ' 20:06'

import xadmin

from xadmin import views
from .models import EmailVerifyRecord,Banner

#设置全局变量--主题
class BaseSetting(object):     #无法使用
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = 'guet在线学习系统'
    site_footer = 'guet在线学习系统'
    menu_style = 'accordion'

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['tilte', 'url', 'index', 'add_time']
    search_fields = ['tilte', 'url', 'index']
    list_filter = ['tilte', 'url', 'index', 'add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
