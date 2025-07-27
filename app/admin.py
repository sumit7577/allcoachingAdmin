from django.contrib import admin
from app.models import *
from django.utils.safestring import mark_safe
import json


class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course","created_at")  # Remove metadata
    
    def display_metadata(self, obj):
        """Ensure metadata is always displayed correctly in admin."""
        return str(obj.metadata)

    display_metadata.short_description = "Metadata (JSON)"  # Admin panel label


class TestSeriesAdmin(admin.ModelAdmin):
    list_display = ("id","name")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone","email","is_institute")
    search_fields = ("username", "email")

    def last_login(self, obj):
        return obj.last_login.strftime("%Y-%m-%d %H:%M:%S") if obj.last_login else None


class TestSeriesAttemptAdmin(admin.ModelAdmin):
    list_display = ("id","test_series","total_score","user","rank","percentile","submitted")
    list_filter = ("test_series",)


class AuthTokenAdmins(admin.ModelAdmin):
    list_display = ("key","user","created","user_is_institute")

    def user_is_institute(self, obj):
        return obj.user.is_institute
    user_is_institute.short_description = "Is Institute"
    user_is_institute.admin_order_field = "user__is_insitute"


class CourseAdmins(admin.ModelAdmin):
    list_display = ("id","name","institute")
    
    
# Register the model with the custom admin class
admin.site.register(CourseVideos, CourseVideoAdmin)
admin.site.register(AuthToken,AuthTokenAdmins)
admin.site.register(User,UserAdmin)
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Course,CourseAdmins)
admin.site.register(VideoLike)
admin.site.register(VideoComment)
admin.site.register(Institute)
admin.site.register(TestSeries,TestSeriesAdmin)
admin.site.register(TestSeriesSolution)
admin.site.register(TestSeriesAttempt,TestSeriesAttemptAdmin)
admin.site.register(Documents)
admin.site.register(CourseLiveStream)
admin.site.register(CommunityPost)
admin.site.register(CommunityComment)
admin.site.register(CommunityLike)
admin.site.register(Otp)
admin.site.register(Order)
admin.site.register(Schedule)
admin.site.register(Playlist)
admin.site.register(Doubt)
#admin.site.register(InstituteBanners)
#admin.site.register(TestRel)