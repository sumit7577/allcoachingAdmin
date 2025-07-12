from rest_framework import serializers
from app.models import Course,CourseVideos,TestSeries,Documents,Schedule,TestSeriesSolution,CommunityPost


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = "__all__"
        read_only_fields = (
            'id',
            "created_at",
            "updated_at",
            "institute",
        )


class PostsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = "__all__"