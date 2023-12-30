from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate
from .models import Student
from django.core import serializers

# Create your views here.
def home(request):
    return redirect("/admin")

