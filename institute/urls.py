from institute import views
from django.urls import include, path, re_path

urlpatterns = [
    path("", views.InstituteViews.as_view(), name="institute-profile"),
]