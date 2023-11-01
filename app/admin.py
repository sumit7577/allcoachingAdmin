from typing import Any, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from app.models import *

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
   list_display = ("id","title","get_institute")

   def get_institute(self, obj):
        return Institute.objects.get(id=obj.inst_id).name
   
   get_institute.short_description = 'Institute Name'


class CourseVideoAdmin(admin.ModelAdmin):
   list_display = ("id","name","get_course")

   def get_institute(self, obj):
        return Institute.objects.get(id=obj.inst_id).name
   
   def get_course(self, obj):
        return Course.objects.get(id=obj.course_id).title
   
   #get_institute.short_description = 'Institute Name'
   get_course.short_description = "Course Name"

class InsTestSeriesAdmin(admin.ModelAdmin):
   list_display = ("id","title","get_course")

   def get_institute(self, obj):
        return Institute.objects.get(id=obj.inst_id).name
   
   def get_course(self, obj):
        return Course.objects.get(id=obj.course_id).title
   
   #get_institute.short_description = 'Institute Name'
   get_course.short_description = "Course Name"

class CourseDocumentAdmin(admin.ModelAdmin):
   list_display = ("id","name","get_course")

   def get_institute(self, obj):
        return Institute.objects.get(id=obj.inst_id).name
   
   def get_course(self, obj):
        return Course.objects.get(id=obj.course_id).title
   
   #get_institute.short_description = 'Institute Name'
   get_course.short_description = "Course Name"


admin.site.register(Admin)
admin.site.register(AdminBlogs)
admin.site.register(AdminConfig)
admin.site.register(AdminTestSeriesCategory)
admin.site.register(AdminTestSeriesSubCategoryContent)
admin.site.register(AdminTestSubCategories)
admin.site.register(Category)
admin.site.register(ContactUs)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseBanners)
admin.site.register(CourseDocument,CourseDocumentAdmin)
admin.site.register(CourseGoLive)
admin.site.register(CourseTimeTableSubject)
admin.site.register(CourseTimeTableItem)
admin.site.register(CourseVideo,CourseVideoAdmin)
admin.site.register(CourseVideoComments)
admin.site.register(DocumentPlaylist)
admin.site.register(Feed)
admin.site.register(FeedCategory)
admin.site.register(FeedComments)
admin.site.register(FeedImages)
admin.site.register(FeedPollOptions)
admin.site.register(FeedReport)
admin.site.register(HibernateSequence)
admin.site.register(InsLeads)
admin.site.register(InsReview)
admin.site.register(InsSubscription)
admin.site.register(InsTestSeries,InsTestSeriesAdmin)
admin.site.register(InsTestSeriesPlaylist)
admin.site.register(InsTestSeriesQuestions)
admin.site.register(InsTestSeriesUserQuestionResponses)
admin.site.register(InsTestSeriesUserResponseBrief)
admin.site.register(Institute)
admin.site.register(MainBanners)
admin.site.register(Notification)
admin.site.register(Otp)
admin.site.register(Payouts)
admin.site.register(QuestionReport)
admin.site.register(Student)
admin.site.register(StudentHistory)
admin.site.register(StudentMessage)
admin.site.register(StudentMessageImages)
admin.site.register(StudentPinList)
admin.site.register(TestSeriesQuestionResponse)
admin.site.register(TestSeriesResponse)
admin.site.register(Transaction)
admin.site.register(VideoPlaylist)
admin.site.register(Coupon)


