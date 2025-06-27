from django.urls import include, path, re_path
from app import views


urlpatterns = [
    path("",views.home),
    path("webhook-video/",views.WebhookVideo.as_view()),
    path('v1/educator/login/', include('user.urls')),
    path('v1/educator/institute/', include('institute.urls')),
    #path("webhook-livestream/",views.UploadLiveStream.as_view()),
]