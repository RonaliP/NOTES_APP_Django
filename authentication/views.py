from django.db.migrations import serializer
from django.shortcuts import HttpResponse, render,redirect
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer,\
    EmailVerificationSerializer,LoginSerializer,\
    ResetPasswordSerializer,NewPasswordSerializer,UserProfileSerializer

from django.contrib.auth import logout,login, authenticate
from rest_framework.response import Response
from authentication.models import User,Profile
from authentication.utils import Util
from django.contrib.sites.shortcuts import  get_current_site
from django.urls import reverse
from django.conf import settings
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework.permissions import AllowAny

# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        try:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
                #token = jwt.encode({'message': 'Hello'}, app.config['SECRET_KEY']).decode('UTF-8')
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = 'Hi' + user.username + 'Use this below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify you email'}
            Util.send_email(data)
            return Response(user_data,status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e




#The below code will verify the email and activate the token sent to user's emailid
#
class VerifyEmailid(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)


            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            return Response({'email': 'Succefully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)





class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'], password=user_data['password'])
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        user_data['token'] = token
        login(request, user)
        return Response(user_data, status=status.HTTP_200_OK)

    
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        current_site = get_current_site(request).domain
        reverseLink = reverse('new-password')
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')

        reset_link = ('http://' + current_site + reverseLink + '?token=' + str(token))
        email_body = "hii \n" + user.username + "Use this link to reset password: \n" + reset_link
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': "Reset password Link"}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_200_OK)


class NewPassword(generics.GenericAPIView):
    serializer_class = NewPasswordSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request):
        token = request.GET.get('token')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.password = user_data['password']
            user.save()
            return Response({'+'
                             ''
                             '+'
                             'email': 'New password is created'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        logout(request)
        return Response({"success": " you are logged out now."},status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset=Profile.objects.all()



    def perform_create(self):
        return serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.profile