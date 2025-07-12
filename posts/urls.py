from posts import views
from django.urls import include, path, re_path


urlpatterns = [
    path("", views.PostsView.as_view(), name="institute-posts"),
    path("<int:pk>/", views.PostsUpdateView.as_view(), name="institute-posts-update"),
]