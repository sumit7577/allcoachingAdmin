from django.shortcuts import render
from user.auth import CustomAuthentication,IsAuthAndTeacher
from rest_framework.generics import *
from institute.serializer import *
from rest_framework.authentication import SessionAuthentication
from app.models import Institute,Course,Category
from rest_framework.response import Response
from django.db.models import Count 
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class InstituteViews(RetrieveUpdateAPIView):
    serializer_class = InstituteSerialzier
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def get_object(self):
        institute, created = Institute.objects.select_related("user", "category", "banner").annotate(follower_count=Count('users')).get_or_create(user=self.request.user)
        return institute
    
    def retrieve(self, request, *args, **kwargs):
        inst = self.get_object()
        serializer = InstituteReadSerializer(inst)
        return Response({
            "status": "true",
            "message": "Institute fetched successfully",
            "data": serializer.data
        })

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


class InstituteCategoryViews(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Category.objects.all().order_by("name")
    

class InstituteFreeContentViews(ListAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseReadSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Course.objects.select_related("category").prefetch_related("banners").annotate(enrolled_count=Count("users")).filter(institute__user=self.request.user,price=0).order_by("-created_at")