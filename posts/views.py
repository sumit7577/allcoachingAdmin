from django.shortcuts import render
from user.auth import CustomAuthentication,IsAuthAndTeacher
from rest_framework.generics import *
from posts.serializer import *
from rest_framework.pagination import PageNumberPagination
from app.models import CommunityPost
from rest_framework.response import Response

# Create your views here.
class PostsView(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = PostsSerializer
    pagination_class = PageNumberPagination


    def perform_create(self, serializer):
        # Automatically attach the institute for the authenticated user
        institute = getattr(self.request.user, "institute", None)
        if not institute:
            raise ValidationError("User is not associated with any institute.")

        serializer.save(institute=institute)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostsReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return CommunityPost.objects.filter(institute__user=self.request.user).order_by("-created_at")
    

class PostsUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = PostsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostsReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        self.pk = self.kwargs.get("pk")
        return CommunityPost.objects.filter(institute__user=self.request.user,id=self.pk).order_by("-created_at")