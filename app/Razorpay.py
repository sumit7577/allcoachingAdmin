import requests
from django.conf import settings
import json

class RazorPay:
    API_KEY = getattr(settings, "RAZORPAY_API_KEY", None)
    API_SECRET = getattr(settings, "RAZORPAY_API_SECRET", None)

    def __init__(self, url: str,payload):
        self.url = url
        self.payload = payload
        self.session = requests.Session()
        self.session.auth = (self.API_KEY, self.API_SECRET)
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def makeRequest(self):
        try:
            response = self.session.post(self.url, data=json.dumps(self.payload))
            response.raise_for_status()
            return {"status":True,"data":response.json()}
        except requests.RequestException as e:
            print(e)
            return {"status":False,"error":response.json()}