#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u'课程名称')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    teacher = models.ForeignKey(Teacher,verbose_name=u'讲师',null=True,blank=True)
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj',u'初级'),('zj',u'高级'),('gj','高级')),max_length=2,verbose_name=u'难度')
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时常（分钟数）')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    category = models.CharField(max_length=20,verbose_name=u'课程类别',default=u'后端开发')
    tag = models.CharField(max_length=10, verbose_name=u'课程标签',default=u'')
    youneed_know = models.CharField(max_length=300,verbose_name=u'课程须知',default=u'')
    teacher_tell = models.CharField(max_length=300, verbose_name=u'老师告诉你', default=u'')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
         return self.usercourse_set.all()[:3]

    def get_lesson(self):
        #获取课程章节
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        #获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='章节名')
    name = models.CharField(max_length=100,verbose_name=u'视频名')
    url = models.CharField(max_length=200,verbose_name=u'访问地址',default=u'')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时常（分钟数）')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名')
    download = models.FileField(upload_to='course/%Y/%m',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name



