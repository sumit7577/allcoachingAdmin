from institute import views
from django.urls import include, path, re_path

urlpatterns = [
    path("", views.InstituteViews.as_view(), name="institute-profile"),
    path("link/", views.InstituteLinkAccount.as_view(), name="institute-account-link"),
    path("category/", views.InstituteCategoryViews.as_view(), name="institute-category"),
    path("free-content/", views.InstituteFreeContentViews.as_view(), name="institute-free-content"),
]