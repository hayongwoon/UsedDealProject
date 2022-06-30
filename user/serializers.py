from dataclasses import field
from django.urls import is_valid_path
from rest_framework import serializers
from user.models import User as UserModel
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel

        fields = ["username", "password", "phone", "fullname"]

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            fullname=validated_data['fullname'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = UserModel
        fields = ["username", "password", "token"]

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = authenticate(username=username, password=password)

        if user is None:
            return {
                'username': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload) # 토큰 발행
            update_last_login(None, user)

        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }

