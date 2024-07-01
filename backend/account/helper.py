
import random
import string
from django.utils.text import slugify
from io import BytesIO
import os
from twilio.rest import Client
from backend import settings


    



account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN 



class MessageHandler:
   
    def send_otp_on_phone(phone,OTP):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body=f'your OTP is {OTP}',
                from_='+12153058792',
                to=phone
             )
        print("otp sent baby")
        print(message.sid)
        