from django.shortcuts import render
from user.auth import CustomAuthentication,IsAuthAndTeacher
from rest_framework.generics import CreateAPIView,UpdateAPIView,GenericAPIView
from institute.serializer import InstituteSerialzier
from rest_framework.authentication import SessionAuthentication
from app.models import Institute
from rest_framework.response import Response

# Create your views here.
class InstituteViews(UpdateAPIView):
    serializer_class = InstituteSerialzier
    authentication_classes = [CustomAuthentication, SessionAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def get_object(self):
        institute,created = Institute.objects.get_or_create(user = self.request.user)
        return institute

    def update(self, request, *args, **kwargs):
        ins = self.get_object()
        serializer = self.get_serializer(ins, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": "true",
            "message": "Profile updated successfully",
            "data": serializer.data
        })