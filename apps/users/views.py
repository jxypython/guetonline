# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord,Banner
from django.db.models import Q
from django.views.generic import View
from .form import LoginForm,RegisterForm,UploadImageForm,ForgetPwdForm,ModifyPwdForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_email
from utils.mixin_utils import LoginRequireMixin
from django.http import HttpResponse,HttpResponseRedirect
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)| Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self,request,active_code):
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            for record in all_code:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):

    def get(self,request):
        registerform = RegisterForm()
        return render(request, "register.html", {'registerform':registerform})

    def post(self,request):
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():   #注册流程
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'registerform':registerform, 'msg': '用户已存在！'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            send_email(user_name, 'register')
            user_profile.save()
            #写入欢迎用户注册消息
            usermessage = UserMessage()
            usermessage.user = user_profile.id
            usermessage.message = '欢迎注册'
            usermessage.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'registerform':registerform})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))



class LoginView(View):

    def get(self,request):
        return render(request, "login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)  # 验证这两个数据和数据库是否相同
            if user is not None:
                if user.is_active:
                    login(request, user)  # 调用该方法进行登录
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html',{'msg': u'用户未激活！'})
            else:
                return render(request, "login.html", {'msg': u'用户名或者密码错误！'})
        else:
            return render(request, "login.html", {'login_form': login_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetPwdForm
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            for record in all_code:
                email = record.email
                return render(request, "password_reset.html",{'email':email })
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    修改用户密码，用于用户未登录的情况在进行密码的修改
    """
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email':email, 'msg': '密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {'email': email, 'modifypwd_form': modifypwd_form })



# class LoginUnSaveView(View):
#     def get(self,request):
#         return render(request, "login.html", {})
#
#     def post(self,request):
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         import MySQLdb
#         conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd= 'zaq1XSW2', db= 'guetonline',charset= 'utf8')
#         cursor = conn.cursor()
#         sql_select = "select * from users_userprofile WHERE email='{0}' and password={1}".format(user_name,pass_word)
#         result = cursor.execute(sql_select)
#         #查询到用户
#         for row in cursor.fetchall():
#             pass

# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         user = authenticate(username= user_name,password= pass_word) #验证这两个数据和数据库是否相同
#         if user is not None:
#             login(request,user) #调用该方法进行登录
#             return render(request,'index.html')
#         else:
#             return render(request, "login.html", {'msg':u'用户名或者密码错误！'})
#     elif request.method == 'GET':
#         return render(request,"login.html",{})


class UserInfoView(LoginRequireMixin, View):
    """
    用户个人信息
    """
    def get(self,request):
        return render(request, 'usercenter-info.html', {
        })

    def post(self,request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')


class UploadImageView(LoginRequireMixin,View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance= request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type='application/json')


class UpdatePwdView(View):
    """
    在个人中心修改密码
    """
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail','msg':'密码不一致'}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse("{'status':'success','msg':'修改成功'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors), content_type='application/json')


class MyCourseView(LoginRequireMixin, View):
    """
    我的课程
    """

    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,
        })


class MyFavOrgView(LoginRequireMixin, View):
    """
    我的收藏课程机构
    """
    def get(self,request):
        org_list = []
        user_favorgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in user_favorgs:
            org_id = fav_org.id
            org = CourseOrg.objects.filter(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequireMixin, View):
    """
    我的收藏教师
    """
    def get(self,request):
        teacher_list = []
        user_favteachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in user_favteachers:
            teacher_id = fav_teacher.id
            favteacher = Teacher.objects.filter(id=teacher_id)
            teacher_list.append(favteacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequireMixin, View):
    """
    我的收藏课程
    """
    def get(self,request):
        course_list = []
        user_favcourses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in user_favcourses:
            course_id = fav_course.id
            favcourse = Course.objects.filter(id=course_id)
            course_list.append(favcourse)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequireMixin, View):
    """
    我的收藏课程
    """
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        all_unread_massage = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_massage in all_unread_massage:
            unread_massage.has_read = True
            unread_massage.save()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages':messages,
        })


class IndexView(View):

    def get(self,request):
        #取出轮播图
        all_banner = Banner.objects.all().order_by('index')
        all_course = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html',{
            'all_banner':all_banner,
            'all_course':all_course,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })


