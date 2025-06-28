from rest_framework.serializers import ModelSerializer
from app.models import Institute,Category,Banner
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' # Or specify the fields you want to expose

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__' # Or specify the fields you want to expos


class InstituteSerialzier(ModelSerializer):
    class Meta:
        model = Institute
        fields = (
            "id",
            'name',
            'about',
            'director_name',
            'image',
            'user',
            'category',
            'banner',
            'date_created',
            'date_updated',
        )
        read_only_fields = (
            'id',
            "user",
            "date_created",
            "date_updated",
        )
    
class InstituteReadSerializer(ModelSerializer):
    follower_count = serializers.IntegerField(read_only=True)
    class Meta:
        depth = 1
        model = Institute
        fields = (
            "id",
            'name',
            'about',
            'director_name',
            'image',
            'user',
            'category',
            'banner',
            'follower_count',
            'date_created',
            'date_updated',
        )
        read_only_fields = (
            'id',
            "user",
            "follower_count",
            "date_created",
            "date_updated",
        )