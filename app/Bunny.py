from tusclient import client
import hashlib
import time
import requests,os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TusFileUploader():
    STREAM_URL=  "https://video.bunnycdn.com/tusupload"
    BASE_URL = "https://video.bunnycdn.com/library/131897/videos"
    API_KEY = "5c48b321-56b9-4071-bcdffc1a0084-6f14-4d42"
    
    def __init__(self) -> None:
        self.client = client.TusClient(self.STREAM_URL)
        self.session = requests.session()


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
        header = {"AccessKey":self.API_KEY,"Content-Type":"application/*+json","accept":"application/json"}
        body = {"title":filename}
        res = self.session.post(url=self.BASE_URL,json=body,headers=header)
        return res.json()

    def create_headers(self,libraryId,videoId):
        expiryTime = time.time()+800
        headers = [str(libraryId),self.API_KEY,str(int(expiryTime)),str(videoId)]
        return headers


    def create_signature(self,headers):
        params = ''.join(headers)
        signature = hashlib.sha256(params.encode("utf-8")).hexdigest()
        return signature