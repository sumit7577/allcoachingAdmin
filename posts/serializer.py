from rest_framework import serializers
from app.models import CommunityPost,CommunityComment,CommunityLike


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


class PostsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "post",
            "comment",
            "created_at",
            "updated_at"
        )

class PostsCommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = (
            "id",
            "user",
            "comment",
            "created_at",
            "updated_at"
        )
        depth = 1



class PostsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityLike
        fields = "__all__"
        read_only_fields = (
            'id',
            "user",
            "post",
            "created_at",
            "updated_at",
            "institute",
        )


class PostsLikeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityLike
        fields = (
            "id",
            "user",
            "created_at",
            "updated_at"
        )
        depth = 1