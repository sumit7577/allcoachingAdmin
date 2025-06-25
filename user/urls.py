from user import views
from django.urls import include, path, re_path

urlpatterns = [
    path("login", views.LoginView.as_view(), name="educator-login"),
    path("verify", views.LoginVerifyView.as_view(), name="educator-login-verify"),
]