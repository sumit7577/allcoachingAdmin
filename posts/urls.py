from posts import views
from django.urls import include, path, re_path


urlpatterns = [
    path("", views.PostsView.as_view(), name="institute-posts"),
    path("<int:pk>/", views.PostsUpdateView.as_view(), name="institute-posts-update"),
    path("<int:pk>/comments/", views.PostsCommentView.as_view(), name="institute-posts-comments"),
    path("<int:pk>/comments/<int:comment>/", views.PostsCommentUpdateView.as_view(), name="institute-posts-comments-update"),
    path("<int:pk>/likes/", views.PostsLikeView.as_view(), name="institute-posts-likes"),
    path("<int:pk>/likes/<int:like>/", views.PostsLikeUpdateView.as_view(), name="institute-posts-likes-update"),
]