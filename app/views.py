from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from django.contrib.auth import authenticate
from .models import Student
from django.core import serializers
from rest_framework.views import APIView
from app.models import *
from app.Cloudfare import CloudfareSdk
import time
from app.Bunny import TusFileUploader
import os
from django.utils import timezone

# Create your views here.
def home(request):
    return redirect("/admin")


def file(request):
    return FileResponse(open("uploads.zip","rb"))



class UploadLiveStream(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        stream_input = LiveStream.objects.get(uid=data["liveInput"])
        fileName = data["meta"]['name'].replace(" ","--")+".mp4"
        cloudfareApi = CloudfareSdk()
        resp = cloudfareApi.createDownload(request.data.get("uid"))
        while(resp['result']['default']['percentComplete']!= 100):
            time.sleep(5)
            resp = cloudfareApi.createDownload(request.data.get("uid"))
        fileObject = cloudfareApi.createToken(request.data.get("uid"))
        with open("default.mp4",mode="wb") as file:
            file.write(fileObject)
        with open("default.mp4",mode="rb") as downloaded:
            bunnyApi = TusFileUploader()
            video = bunnyApi.upload(downloaded,fileName)
            fileNameCourse = f"files/{video[0]["guid"]}--{fileName}"
            id= CourseVideo.objects.all()
            courseCreated = CourseVideo.objects.create(id=len(id)+1,date=timezone.now(),course_id=stream_input.course.id,playlist_id=0,
                                       video_location=fileNameCourse,video_type="offline",
                                       views=0,length=data['duration'],encoded=0,name=stream_input.course.title,time_stamp=timezone.now())
            courseCreated.save()
        
        os.remove("default.mp4")

        return JsonResponse({"status":True,"data":request.data})


