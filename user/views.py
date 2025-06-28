from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from app.models import *
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.response import Response
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import CreateAPIView,UpdateAPIView,GenericAPIView
from rest_framework.parsers import MultiPartParser
from user.serializer import * 
from app.models import *
import random
from user.service import send_otp
from user.auth import CustomAuthentication,IsAuthAndTeacher
from app.manager import generate_random_username

def generate_otp():
    return f"{random.randint(0, 999999):06}"


class LoginView(CreateAPIView):
    serializer_class = AuthSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp = generate_otp()

        if not send_otp(phone, otp):
            return Response(
                {"status": "false", "message": "Failed to send OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        otp_instance = Otp.objects.create(phone=phone, otp=otp)
        serialized_otp = OTPSerializer(otp_instance)

        return Response({
            "status": "true",
            "message": "OTP sent successfully",
            "data": serialized_otp.data
        })


class LoginVerifyView(CreateAPIView):
    serializer_class = LoginVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        try:
            otp_instance = Otp.objects.get(phone=phone, otp=otp)
        except Otp.DoesNotExist:
            return Response(
                {"status": "false", "message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(phone=phone).first()
        user_created = False

        if user:
            if not getattr(user, "is_institute", False):
                return Response(
                    {"status": "false", "message": "Only educators are allowed to log in."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            try:
                with transaction.atomic():
                    user = User.objects.create(phone=phone, is_institute=True,username=generate_random_username(""))
                    token = AuthToken.objects.create(user=user)
                    ins = Institute.objects.create(user=user)
                    user_created = True
            except Exception as e:
                return Response(
                    {"status": "false", "message": f"Failed to create user/token: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        user = User.objects.get(phone=phone)
        token= AuthToken.objects.select_related("user").get(user = user)
        serialized_token = AuthTokenSerializer(token)
        otp_instance.delete()
        return Response({
            "status": "true",
            "message": "No user found" if user_created else "Login successful",
            "data": serialized_token.data
        })
    

class CompleteSignupView(UpdateAPIView):
    serializer_class = CompleteSignupSerializer
    authentication_classes = [CustomAuthentication, SessionAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        new_name = serializer.validated_data.get("name")
        if new_name:
            user.username = generate_random_username(new_name)
        response = UserSerializer(user)
        serializer.save()

        return Response({
            "status": "true",
            "message": "Profile updated successfully",
            "data": response.data
        })