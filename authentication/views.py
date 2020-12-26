from django.shortcuts import render
from rest_framework import generics,status,views
from .serializers import RegisterSerializer,EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer


    def post(self,request):

        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data

       #added below  lines to access the email of user

        user=User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token

        current_site=get_current_site(request).domain
        relativeLink=reverse('email-verify')
        absurl = 'http://' + current_site + \
                 relativeLink + "?token=" + str(token)
        email_body='Hey'+ user.username +\
                   'use link below to verify your email and activate your account\n'+ \
                   absurl
        data={'email_body':email_body,
              'to_email':user.email,
              'email_subject':'verify email'}
        Util.send_email(data)


        return Response(user_data,status=status.HTTP_201_CREATED)


#The below code will verify the email and activate the token sent to user's emailid
#
class VerifyEmailid(views.APIView):
    serializer_class=EmailVerificationSerializer
    token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',
                                         type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])


    def get(self, request):
        token = request.GET.get('token')
        # now from above line i got access to the token ,now we'll try to decode it

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=decoded['user_id'])
            if not user.is_verified:
                user.is_active = True
                user.is_verified = True
                user.save()
            return Response({'email': 'Succefully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)