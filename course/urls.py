from course import views
from django.urls import include, path, re_path


urlpatterns = [
    path("", views.CourseView.as_view(), name="institute-course"),
    path("<int:pk>/", views.CourseUpdateView.as_view(), name="institute-course-update"),
    path("<int:pk>/videos/", views.CourseVideosView.as_view(), name="institute-course-videos"),
    path("<int:pk>/videos/<int:video>/", views.CourseVideosUpdateView.as_view(), name="institute-course-videos-update"),
    path("<int:pk>/testSeries/", views.CourseTestSeriesView.as_view(), name="institute-course-testSeries"),
    path("<int:pk>/testSeries/<int:test>/", views.CourseTestSeriesUpdateView.as_view(), name="institute-course-test-update"),
    path("<int:pk>/documents/", views.CourseDocumentsView.as_view(), name="institute-course-document"),
    path("<int:pk>/documents/<int:document>/", views.CourseDocumentUpdateView.as_view(), name="institute-course-document-update"),
    path("<int:pk>/schedules/", views.CourseScheduleView.as_view(), name="institute-course-schedules"),
    path("<int:pk>/schedules/<int:schedule>/", views.CourseSchedulesUpdateView.as_view(), name="institute-course-schedules-update"),
]