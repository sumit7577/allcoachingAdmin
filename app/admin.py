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

# Register the model with the custom admin class
admin.site.register(CourseVideos, CourseVideoAdmin)
admin.site.register(AuthToken)
admin.site.register(User)
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Institute)
#admin.site.register(InstituteBanners)
#admin.site.register(TestRel)