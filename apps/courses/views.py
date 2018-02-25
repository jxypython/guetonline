# _*_encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import Course,CourseResource,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,CourseComment,UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequireMixin
from django.db.models import Q
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-click_nums')[:3]
        #课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course=all_course.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|
                                         Q(detail__icontains=search_keywords))
        #课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')
        # 课程数

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)
        course = p.page(page)
        return render(request,'course-list.html',{
            'all_course': course,
            'sort':sort,
            'hot_course':hot_course,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_nums+=1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequireMixin, View):
    """
    课程章节信息
    """
    def get(self,request,course_id):
        hav_lesson = 'lesson'
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resourse = CourseResource.objects.filter(course=course)
        #查询该用户是否以及关联了该用户
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'all_resourse': all_resourse,
            'relate_courses': relate_courses,
            'hav_lesson':hav_lesson,
        })


class CommentView(LoginRequireMixin, View):
    """
       评论信息
    """

    def get(self, request, course_id):
        hav_comment = 'comment'
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #获取该用户学过的其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resourse = CourseResource.objects.filter(course=course)
        all_comment = CourseComment.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resourse': all_resourse,
            'all_comment':all_comment,
            'relate_courses': relate_courses,
            'hav_comment':hav_comment,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self,request):
        if not request.user.is_authenticated:
            #判断用户登录状态
            return HttpResponse("{'status':'fail','msg':'用户未登录'}", content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id= int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse("{'status':'success','msg':'评论成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'评论失败'}", content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面    
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resourse = CourseResource.objects.filter(course=course)
        # 查询该用户是否以及关联了该用户
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, 'course_play.html', {
            'course': course,
            'all_resourse': all_resourse,
            'relate_courses': relate_courses,
            'video':video,
        })




