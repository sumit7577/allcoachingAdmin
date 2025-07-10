from django.shortcuts import render
from user.auth import CustomAuthentication,IsAuthAndTeacher
from rest_framework.generics import *
from course.serliazer import *
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from app.models import Course,CourseVideos,TestSeries,Documents
from rest_framework.response import Response

# Create your views here.
class CourseView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Course.objects.select_related("category").prefetch_related("banners").annotate(enrolled_count=Count("users")).filter(institute__user=self.request.user,price__gt=0).order_by("-created_at")
    

class CourseUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return Course.objects.select_related("category").prefetch_related("banners").annotate(enrolled_count=Count("users")).filter(institute__user=self.request.user,id=self.pk).order_by("-created_at")
    

class CourseVideosView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseVideosSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseVideosReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        # Get the course_id from URL kwargs (e.g., from /courses/<int:course_pk>/videos/)
        course_id = self.kwargs.get("pk")

        if not course_id:
            # This should ideally be caught by URL routing or permissions,
            # but as a safeguard.
            raise serializers.ValidationError({"detail": "Course ID not provided in URL."})

        # Ensure the course exists and belongs to the authenticated user's institute
        # before associating the video with it.
        try:
            course = get_object_or_404(
                Course,
                id=course_id,
                institute__user=self.request.user
            )
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Course with this ID does not exist or you do not have permission to add videos to it."})

        serializer.save(course=course)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return CourseVideos.objects.select_related("playlist").filter(course__institute__user=self.request.user,course__id=self.pk).order_by("-created_at")
    

class CourseVideosUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseVideosSerializer
    lookup_url_kwarg = "video"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseVideosReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        course_id = self.kwargs.get("pk") # This should be the ID of the Course
        video_id = self.kwargs.get("video")
        return CourseVideos.objects.select_related("playlist").filter(course__institute__user=self.request.user,id=video_id)
    


class CourseTestSeriesView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseTestSeriesSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseTestSeriesReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        # Get the course_id from URL kwargs (e.g., from /courses/<int:course_pk>/videos/)
        course_id = self.kwargs.get("pk")

        if not course_id:
            # This should ideally be caught by URL routing or permissions,
            # but as a safeguard.
            raise serializers.ValidationError({"detail": "Course ID not provided in URL."})

        # Ensure the course exists and belongs to the authenticated user's institute
        # before associating the video with it.
        try:
            course = get_object_or_404(
                Course,
                id=course_id,
                institute__user=self.request.user
            )
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Course with this ID does not exist or you do not have permission to add videos to it."})

        serializer.save(course=course)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return TestSeries.objects.select_related("playlist").filter(course__institute__user=self.request.user,course__id=self.pk).order_by("-created_at")
    

class CourseTestSeriesUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseTestSeriesSerializer
    lookup_url_kwarg = "test"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseTestSeriesReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        course_id = self.kwargs.get("pk") # This should be the ID of the Course
        test_id = self.kwargs.get("test")
        return TestSeries.objects.select_related("playlist").filter(course__institute__user=self.request.user,id=test_id)
    


class CourseDocumentsView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseDocumentsSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseDocumentsReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        # Get the course_id from URL kwargs (e.g., from /courses/<int:course_pk>/videos/)
        course_id = self.kwargs.get("pk")

        if not course_id:
            # This should ideally be caught by URL routing or permissions,
            # but as a safeguard.
            raise serializers.ValidationError({"detail": "Course ID not provided in URL."})

        # Ensure the course exists and belongs to the authenticated user's institute
        # before associating the video with it.
        try:
            course = get_object_or_404(
                Course,
                id=course_id,
                institute__user=self.request.user
            )
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Course with this ID does not exist or you do not have permission to add videos to it."})

        serializer.save(course=course)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return Documents.objects.select_related("playlist").filter(course__institute__user=self.request.user,course__id=self.pk).order_by("-created_at")
    

class CourseDocumentUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseDocumentsSerializer
    lookup_url_kwarg = "document"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseDocumentsReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        course_id = self.kwargs.get("pk") # This should be the ID of the Course
        doc_id = self.kwargs.get("document")
        return Documents.objects.select_related("playlist").filter(course__institute__user=self.request.user,id=doc_id)
    

class CourseScheduleView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseScheduleSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseScheduleReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        # Get the course_id from URL kwargs (e.g., from /courses/<int:course_pk>/videos/)
        course_id = self.kwargs.get("pk")

        if not course_id:
            # This should ideally be caught by URL routing or permissions,
            # but as a safeguard.
            raise serializers.ValidationError({"detail": "Course ID not provided in URL."})

        # Ensure the course exists and belongs to the authenticated user's institute
        # before associating the video with it.
        try:
            course = get_object_or_404(
                Course,
                id=course_id,
                institute__user=self.request.user
            )
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Course with this ID does not exist or you do not have permission to add videos to it."})

        serializer.save(course=course)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return Schedule.objects.filter(course__institute__user=self.request.user,course__id=self.pk).order_by("-created_at")
    

class CourseSchedulesUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseScheduleSerializer
    lookup_url_kwarg = "schedule"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseScheduleReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        course_id = self.kwargs.get("pk") # This should be the ID of the Course
        schedule_id = self.kwargs.get("schedule")
        return Schedule.objects.filter(course__institute__user=self.request.user,id=schedule_id)