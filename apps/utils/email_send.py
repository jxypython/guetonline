# _*_ encoding:utf-8 _*_
__author__ = 'jiangxiaoyan'
__data__ = ' 15:05'

from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from guetonline.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFeGgHhIiJjKkMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    myrandom_str =random_str(16)
    email_record.code = myrandom_str
    email_record.email = email
    email_record.send_type =send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'guet在线学习系统注册激活连接'
        email_body = '请点击下面的连接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(myrandom_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email],fail_silently=False)
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = 'guet在线学习系统密码重置激活连接'
        email_body = '请点击下面的连接激活你的账号：http://127.0.0.1:8000/reset/{0}'.format(myrandom_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], fail_silently=False)
        if send_status:
            pass