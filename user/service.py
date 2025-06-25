import random
from app.models import Otp
from django.conf import settings
import requests

def send_otp(phone: str, otp: str) -> bool:
    # For testing / demo phone
    if phone == "9889977262":
        return "OTP sent successfully"

    # Delete old OTPs for this phone
    Otp.objects.filter(phone=phone).delete()

    # Load config from Django settings
    api_url = getattr(settings, "SMS_API_URL", None)
    api_key = getattr(settings, "SMS_API_KEY", None)

    if not api_url or not api_key:
        raise Exception("SMS API URL or API KEY not configured in settings")

    # Build the request URL
    message = "184022"  # Template ID or message ID
    sender_id = "AllCOG"
    full_url = (
        f"{api_url}?authorization={api_key}&sender_id={sender_id}"
        f"&message={message}&variables_values={otp}&route=dlt&numbers={phone}"
    )

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        #raise Exception(f"Failed to send OTP: {e}")
        return False