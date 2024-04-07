from django.urls import include, path, re_path
from app import views


urlpatterns = [
    path("webhook-livestream/",views.UploadLiveStream.as_view()),
]