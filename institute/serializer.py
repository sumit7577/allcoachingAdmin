from rest_framework.serializers import ModelSerializer
from app.models import Institute

class InstituteSerialzier(ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"
        read_only_fields = (
            'id',
            "user",
            "users",
            "date_created",
            "date_updated",
        )