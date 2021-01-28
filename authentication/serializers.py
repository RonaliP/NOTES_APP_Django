from rest_framework import serializers
from authentication.models import User,Profile
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)

    class Meta:
        model =User
        fields =['firstname','lastname','email','username' ,'password']

    def validate(self ,attrs):
        email =attrs.get('email' ,'')
        username =attrs.get('username' ,'')

        if not username.isalnum():
            raise serializers.ValidationError('username must only contain alphanumeric')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user




class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=700)

    class Meta:
        model =User
        fields =['token']

class LoginSerializer(serializers.ModelSerializer):
    email =serializers.EmailField()
    password =serializers.CharField(min_length=3)


    class Meta:
        model =User
        fields =['email' ,'password']

    def validate(self ,attrs):
        email =attrs.get('email' ,'')
        password =attrs.get('password' ,'')

        try:


            user = User.objects.get(email=email, password=password)
            if not user:
                raise AuthenticationFailed('INVALID DATA GIVEN,TRY AGAIN')
            if not user.is_active:
                raise AuthenticationFailed('ACCOUNT IS NOT ACTIVATED YET')
            if not user.is_verified:
                raise AuthenticationFailed('EMAIL ID IS NOT VERIFIED YET')

        except serializers.ValidationError as identifier:
            return {'error': "check with your email and password"}

        return {
            'email': user.email,
            'password': user.password,
        }

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                raise serializers.ValidationError("This email id is not verified!!")
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registerd")

        return attrs


class NewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    NewPassword=serializers.CharField(max_length=68, min_length=6)


    class Meta:
        model = User
        fields = ['password', 'NewPassword']

    def validate(self, attrs):
        password = attrs.get('password', '')
        NewPassword =attrs.get('NewPassword', '')

        if password != NewPassword:
            raise serializers.ValidationError("Password not matched!!")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['DOB', 'image', 'user_id']




