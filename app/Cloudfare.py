import time
import requests
import json

class CloudfareSdk():
    
    def __init__(self) -> None:
        self.session = requests.session()
        self.headers = {"Authorization":"Bearer fTNDiYAiY553WzlhwdwKpt8wZv33K7eoF30HTaK1",
                        'Content-Type': 'application/json'}
        self.accountId = "a7ec2a415b9f64a90074628e969d8ef8"
        self.BASE_URL = "https://api.cloudflare.com/client/v4/accounts/"
        self.kid= "34d9cb360be6be4afbdfea675b0825f6"
        self.CUSTOMER_URL = "https://customer-y9o3cvk41jloxspj.cloudflarestream.com/"


    def createDownload(self,videoId:str)->None:
        resp = self.session.post(url=self.BASE_URL+f"{self.accountId}/stream/{videoId}/downloads",
                                 headers=self.headers)
        return resp.json()
    
    def createToken(self,videoId)->None:
        current_time = int(time.time())
        expiration_time = current_time + 3600
        not_before_time = current_time
        restrications = {"sub": videoId,"kid":self.kid,"exp": expiration_time,"nbf": not_before_time,"downloadable": True,
                         "accessRules": [{"type": "ip.geoip.country","action": "allow","country": ["IN"]},{"type": "any","action": "block"}]}
        resp = self.session.post(self.BASE_URL+f"{self.accountId}/stream/{videoId}/token",
                                 headers=self.headers,
                                 data=json.dumps(restrications))
        return self.fileResponse(resp.json()["result"]["token"])
    
    def fileResponse(self,token):
        resp = self.session.get(self.CUSTOMER_URL+f"{token}/downloads/default.mp4")
        return resp.content
