from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        max_length=68,min_length=10,write_only=True)

    class Meta:
        model=User
        fields=['firstname','lastname','email','username','password']

    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('username must only contain alphanumeric')
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=700)

    class Meta:
        model=User
        fields=['token']
