from rest_framework import serializers
from app.models import Course,CourseVideos,TestSeries,Documents,Schedule,TestSeriesSolution,Banner,VideoComment


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


class CourseVideosCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = "__all__"
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "video",
            "user"
        )


class CourseVideosCommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = (
            "id",
            "user",
            "comment",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "video",
            "user"
        )
        depth =1
    

class TestSeriesSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeriesSolution
        fields = ("id", "description", "solution", "created_at", "updated_at")


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
    solution = serializers.SerializerMethodField()
    class Meta:
        model = TestSeries
        fields = (
            "id",
            "name",
            "file",
            "playlist",
            "description",
            "questions",
            "solution",
            "timer",
            "created_at",
            "updated_at"
        )
        depth = 1

    def get_solution(self, obj):
        solution_qs = TestSeriesSolution.objects.filter(test_series=obj)
        return TestSeriesSolutionSerializer(solution_qs, many=True).data
    

class CourseTestSeriesReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeries
        fields = (
            "id",
            "name",
            "file",
            "playlist",
            "description",
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

class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields=(
            'id',
            "created_at",
            "updated_at",
            "course",
        )


class CourseScheduleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
        read_only_fields=(
            "date_created",
            "date_updated",
        )