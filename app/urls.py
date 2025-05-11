from django.urls import include, path, re_path
from app import views


urlpatterns = [
    path("",views.home),
    path("webhook-video/",views.WebhookVideo.as_view())
    #path("webhook-livestream/",views.UploadLiveStream.as_view()),
]