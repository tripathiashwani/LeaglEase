from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import loginSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
import string
from .models import PhoneOTP,CustomUser
from django.utils.text import slugify
from io import BytesIO
from .helper import MessageHandler
from rest_framework.decorators import api_view, authentication_classes, permission_classes


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


    

def otp_generator():
    otp = random.randint(99999, 999999)
    return otp

def send_otp(phone):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:
        
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        return otp_key
    else:
        return False

'''
 if the OTP count is more than 10 then, user has to contact the customer care support.
'''
class SendPhoneOTP(APIView):
    def post(self, *args, **kwargs):
        phone_number = self.request.data.get('phone')
        print(phone_number)
        
        if phone_number:

            phone = str(phone_number)
            user = CustomUser.objects.filter(phone__iexact = phone)
            
            OTP=otp_generator()
            
            print(phone, OTP)
            if OTP: 
                otp = str(OTP)
                old_otp = PhoneOTP.objects.filter(phone__iexact = phone)

                if old_otp.exists():
                    old_otp = old_otp.first()
                    otp_count = old_otp.count

                    if otp_count > 100:
                        return Response ({
                        'status':False,
                        'detail':'You have exceeded the OTP limit. Kindly contact our customer care support.'
                        })

                    old_otp.count = otp_count + 1
                    old_otp.otp = otp
                    old_otp.save()
                    MessageHandler.send_otp_on_phone(phone,OTP)
                    print("count increase", old_otp.count)
                    return Response ({
                    'status':True,
                    'detail':'OTP sent successfully.'
                    })
                
                else:
                    PhoneOTP.objects.create(
                        phone = phone,
                        otp = otp)
                    
                    return Response ({
                    'status':True,
                    'detail':'OTP sent successfully.'
                    })
                        

            else:
                return Response ({
                    'status':False,
                    'detail':'OTP sending error. Please try after sometime'
                    })


        else:
            return Response ({
                'status': False,
                'detail':'No phone number has been received. Kindly do the POST request.'
                })




'''
Validating the OTP which is sent to the user
'''

class ValidateOTP(APIView):
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone',False)
        otp_sent = self.request.data.get('otp',False)
        # print("phone",phone,"otp-sent",otp_sent)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                print("old otp",old," new_otp",otp_sent)
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    tokens=get_tokens_for_user(self.request.user)
                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password',
                        'tokens':tokens
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })

            else:
                return Response({
                    'status' : False,
                    'detail' : 'Incorrect Phone number. Kindly request a new otp with this number'
                })

        else:
            return Response({
                'status' : False,
                'detail' : 'Either phone or otp was not recieved in Post request'
            })

@api_view(['POST'])
def SendNotification(request,pk):
    sent_by=request.user
    send_to=CustomUser.all.filter(pk=pk)
