from rest_framework import serializers 
import re
from django.core.validators import RegexValidator
from app.models import Otp,AuthToken,User

class AuthSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.'
            )
        ]
    )

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['phone', 'otp', 'created']


class LoginVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.'
            )
        ]
    )
    otp = serializers.CharField(
        max_length=6,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='OTP must be exactly 6 digits.'
            )
        ]
    ) 

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = "__all__"
        depth = 1


class CompleteSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","name"]