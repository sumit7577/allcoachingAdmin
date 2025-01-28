import requests
from django.core.files.storage import Storage

class BunnyStorage(Storage):
    CDN_URL = "sg.storage.bunnycdn.com"
    STORAGE_NAME = "allcoaching-bucket"
    ACCESS_KEY = '72082176-d1df-4729-bef6359087c7-bb4d-4ae2'

    def __init__(self,directoryName=""):
        self.directoryName = directoryName
        self.session = requests.session()


    def create_headers(self):
        headers = {"AccessKey": self.ACCESS_KEY,"Content-Type":"application/octet-stream","accept":"application/json"}
        return headers
    
    
    def create_url(self):
       return f"https://{self.CDN_URL}/{self.STORAGE_NAME}/"
    

    def uploadImage(self,fs,filename):
        headers = self.create_headers()
        url = f"{self.create_url()}{self.directoryName}{filename}"
        res = self.session.put(url=url,headers=headers,data=fs)
        if res.status_code == 201:
            return True, f"https://allcoaching-bucket.b-cdn.net/{self.directoryName}{filename}"
        else:
            return False, res.json()
        
        
    def _save(self, name, content):
        """
        Save the given content to the BunnyCDN storage.
        """
        response = self.uploadImage(content, name)
        if response[0]:
            return response[1]
        else:
            raise Exception(response[1])
        
        
    def exists(self, name):
        """
        Skip file existence checks since we don't store files locally.
        """
        return False
    
    def url(self, name):
        """
        Return the URL for the given name (already stored as a string).
        """
        return name
