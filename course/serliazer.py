from rest_framework import serializers
from app.models import Course,CourseVideos,TestSeries,Documents


class CourseReadSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "category",
            "banners",
            "collection",
            "description",
            "price",
            "demo_video",
            "pdf",
            "created_at",
            "updated_at",
            "image",
            "start_date",
            "end_date",
            "faqs",
            "enrolled_count",
        )
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "collection",
            "institute",
            "users",
        )


class CourseVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideos
        fields = "__all__"
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "course",
        )

class CourseVideosReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideos
        fields = (
            "id",
            "name",
            "playlist",
            "description",
            "video",
            "metadata",
            "views",
            "created_at",
            "updated_at",
        )
        depth = 1


class CourseTestSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeries
        fields = "__all__"
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "course",
        )


class CourseTestSeriesReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeries
        fields = (
            "id",
            "name",
            "file",
            "playlist",
            "description",
            "questions",
            "timer",
            "created_at",
            "updated_at"
        )
        depth = 1


class CourseDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
        read_only_fields=(
            'id',
            "created_at",
            "updated_at",
            "course",
        )


class CourseDocumentsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        depth = 1
        fields = (
            "id",
            "playlist",
            "name",
            "description",
            "file",
            "created_at",
            "updated_at"
        )
        