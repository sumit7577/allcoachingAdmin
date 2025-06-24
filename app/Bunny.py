from tusclient import client
import hashlib
import time
import requests,os
from pathlib import Path
from django.core.files.storage import Storage
from django.core.files.storage import FileSystemStorage
import json


BASE_DIR = Path(__file__).resolve().parent.parent
    
class TusFileUploader(Storage):
    STREAM_URL=  "https://video.bunnycdn.com/tusupload"
    BASE_URL = "https://video.bunnycdn.com/library/131897/videos"
    API_KEY = "5c48b321-56b9-4071-bcdffc1a0084-6f14-4d42"
    HLS_URL = "https://vz-466ee95b-26a.b-cdn.net/"
    IFRAME_URL = "https://iframe.mediadelivery.net/play/131897/"
    COLLECTION_URL = "https://video.bunnycdn.com/library/131897/collections"
    
    def __init__(self,instance,*args,**kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client = client.TusClient(self.STREAM_URL)
        self.instance = instance
        self.session = requests.session()

    def __instancecheck__(self):
        from app.models import CourseVideos, Course  # Local import to avoid circular dependency
        
        if isinstance(self.instance, CourseVideos):
            return "CourseVideos"
        else:
            return "Course"


    def set_headers(self,id,libId):
        headers = self.create_headers(libraryId=libId,videoId=id)
        hash = self.create_signature(headers)
        bunnyHeaders = {"Authorizationsignature":hash,"Authorizationexpire":headers[2],"Videoid":headers[3],"Libraryid":headers[0]}
        self.client.set_headers(bunnyHeaders)

    def upload(self,fs,filename):
        video = self.create_video(filename=filename)
        self.set_headers(video['guid'],131897)
        try:
            uploader = self.client.uploader(file_stream=fs)
            uploader.upload()
            return (video,True)
        except Exception as e:
            print(e)
            return False

    def create_video(self,filename):
        header = {"AccessKey":self.API_KEY,"Content-Type":"application/json","accept":"application/json"}
        if self.__instancecheck__() == "CourseVideos":
            collection= self.instance.course.collection
        else:
            collection = self.instance.collection

        body = {"title":filename,"collectionId":collection["guid"]}
        res = self.session.post(url=self.BASE_URL,json=body,headers=header)
        print(res.text)
        return res.json()
    
    def createCollection(self,id):
        header = {"AccessKey":self.API_KEY,"Content-Type":"application/json","accept":"application/json"}
        body = {"name":id}
        res = self.session.post(url=self.COLLECTION_URL,json=body,headers=header)
        if res.status_code ==200:
            return True,res.json()
        else:
            return False,res.json()
    

    def getCollection(self,id):
        header = {"AccessKey":self.API_KEY,"Content-Type":"application/json","accept":"application/json"}
        url = f"{self.COLLECTION_URL}/{id}"
        res = self.session.get(url=url,headers=header)
        print(res.text)
        if res.status_code ==200:
            return True,res.json()
        else:
            return False,res.text
        

    def create_headers(self,libraryId,videoId):
        expiryTime = time.time()+800
        headers = [str(libraryId),self.API_KEY,str(int(expiryTime)),str(videoId)]
        return headers


    def create_signature(self,headers):
        params = ''.join(headers)
        signature = hashlib.sha256(params.encode("utf-8")).hexdigest()
        return signature
    
    def getVideoMetadata(self,videoId):
        url = f"{self.BASE_URL}/{videoId}"
        header = {"AccessKey":self.API_KEY,"Content-Type":"application/json","accept":"application/json"}
        res = self.session.get(url=url,headers=header)
        if res.status_code == 200:
            return True,res.json()
        else:
            return False,res.text

    def _save(self, name, content):
        """
        Save the given content to the BunnyCDN storage.
        """
        response = self.upload(content, name)
        if response[1]:
            data = response[0]
            guid = data["guid"]
            if(self.__instancecheck__() == "CourseVideos"):
                self.instance.metadata = response[0]

            url = f"{self.HLS_URL}{guid}/playlist.m3u8"
            return url
        else:
            raise Exception(response[0])

        
    def exists(self, name):
        """
        Skip file existence checks since we don't store files locally.
        """
        return False
    
    def url(self, name):
        """
        Return the URL for the given name (already stored as a string).
        """
        guid = name.split("/")[3]
        iframe_url = f"{self.IFRAME_URL}{guid}"
        return iframe_url