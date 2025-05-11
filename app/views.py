from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from django.contrib.auth import authenticate
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

class WebhookVideo(APIView):
    def get(self,request,*args,**kwargs):
        return JsonResponse({"status":True,"message":"Api is running"})
    
    def post(self,request,*args,**kwargs):
        data = request.data
        video_guid = data.get('VideoGuid')
        status = data.get('Status')
        if not video_guid or status is None:
            return JsonResponse({"status": False, "message": "Missing VideoGuid or Status", "data": data})
        
        if int(status) == 3:
            storage = TusFileUploader(instance=None)
            videoName = f"{storage.HLS_URL}{video_guid}/playlist.m3u8"
            metadata = storage.getVideoMetadata(video_guid)
            if metadata[0] == True:
                courseVideo = CourseVideos.objects.get(video=videoName)
                if courseVideo is not None:
                    courseVideo.metadata = metadata[1]
                    courseVideo.save()
            
        return JsonResponse({"status":True,"data":metadata[1]})



"""class UploadLiveStream(APIView):

    def get(self,request,*args,**kwargs):
        return JsonResponse({"status":True,"message":"Api is running"})
    
    def post(self,request,*args,**kwargs):
        data = request.data
        liveUid = data.get("liveInput")

        isSaved = LiveStreamLogs.objects.filter(uid=data.get("uid"))
        if len(isSaved) > 0:
            return JsonResponse({"status":True,"data":"Stream already saved"})

        if liveUid is None:
            return JsonResponse({"status":False,"data":data})
        
        stream_input = LiveStream.objects.get(uid=liveUid)
        LiveStreamLogs.objects.create(data=data,uid=data.get("uid")).save()
        fileName = data["meta"]['name'].replace(" ","--")+".mp4"
        cloudfareApi = CloudfareSdk()
        resp = cloudfareApi.createDownload(data.get("uid"))
        if resp is None:
            JsonResponse({"status":True,"data":data})

        if resp['result']['default']['status'] == "error":
            return JsonResponse({"status":False,"data":resp})

        while(resp['result']['default']['percentComplete']!= 100):
            time.sleep(5)
            resp = cloudfareApi.createDownload(data.get("uid"))
        fileObject = cloudfareApi.createToken(data.get("uid"))

        with open("default.mp4",mode="wb") as file:
            file.write(fileObject)

        with open("default.mp4",mode="rb") as downloaded:
            bunnyApi = TusFileUploader()
            video = bunnyApi.upload(downloaded,fileName)
            fileNameCourse = f"files/{video[0]['guid']}--{fileName}"
            max_id = CourseVideo.objects.aggregate(max_id=models.Max('id'))['max_id']
            next_id = 1 if max_id is None else max_id + 1
            courseCreated = CourseVideo.objects.create(id=next_id,date=timezone.now(),course_id=stream_input.course.id,playlist_id=0,
                                       video_location=fileNameCourse,video_type="offline",
                                       views=0,length=data['duration'],encoded=0,name=stream_input.course.title,time_stamp=timezone.now())
            courseCreated.save()
        
        os.remove("default.mp4")

        return JsonResponse({"status":True,"data":data})


"""