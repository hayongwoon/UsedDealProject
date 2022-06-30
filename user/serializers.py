from dataclasses import field
from django.urls import is_valid_path
from rest_framework import serializers
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import WatchList as WatchListModel
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListModel

        fields = ["name"]

class UserProfileSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(read_only=True, many=True, required=False)
    get_watchlist = serializers.ListField(required=False)
    class Meta:
        model = UserProfileModel

        fields = ["introduction", "birthday", "age", "watchlist", "get_watchlist"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    
    class Meta:
        model = UserModel

        fields = ["username", "password", "phone", "fullname", "userprofile"]
        extra_kwargs = {
            "password" : {"write_only" : True},
            }

    def create(self, validated_data):
        userprofile = validated_data.pop('userprofile')
        get_watchlist = userprofile.pop('get_watchlist', [])
        
        user = UserModel.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            fullname=validated_data['fullname'],
        )
        #비밀번호 해시를 위해 set_password
        user.set_password(validated_data['password'])
        user.save()

        userprofile = UserProfileModel.objects.create(user=user, **userprofile)

        userprofile.watchlist.add(*get_watchlist)
        userprofile.save()

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

