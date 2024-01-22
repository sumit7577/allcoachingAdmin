from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from django.contrib.auth import authenticate
from .models import Student
from django.core import serializers

# Create your views here.
def home(request):
    return redirect("/admin")


def file(request):
    return FileResponse(open("uploads.zip","rb"))

