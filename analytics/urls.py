from django.urls import include, path, re_path
from analytics import views

urlpatterns = [
    path("", views.InstituteSales.as_view(), name="institute-sales"),
    path("transactions/", views.InstituteTransactions.as_view(), name="institute-transactions"),
]