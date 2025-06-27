from rest_framework.serializers import ModelSerializer
from app.models import Institute

class InstituteSerialzier(ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"