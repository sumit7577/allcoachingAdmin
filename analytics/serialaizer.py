from rest_framework import serializers
from app.models import Order,Course

class SeriesItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    data = serializers.ListField(child=serializers.IntegerField())

class SalesSerializer(serializers.Serializer):
    categories = serializers.ListField(child=serializers.CharField())
    series = SeriesItemSerializer(many=True)

class CourseSerialiazer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "price"
        )
        model = Course

class OrderSerializer(serializers.ModelSerializer):
    course = CourseSerialiazer()
    class Meta:
        model = Order
        fields= "__all__"
        depth = 1