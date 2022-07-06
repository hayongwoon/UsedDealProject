from dataclasses import field
from django.urls import is_valid_path
from rest_framework import serializers
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import WatchList as WatchListModel
from product.models import Product as ProductModel

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login



class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListModel

        fields = ["name"]

class UserProfileSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(read_only=True, many=True)
    get_watchlist = serializers.ListField(write_only=True, required=False)
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

    def update(self, instance, validated_data):
        userprofile = validated_data.pop('userprofile')
        get_watchlist = userprofile.pop('get_watchlist', [])

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save() 

        # update는 아이디를 반환한다. 따라서 해당 아이디로 객체를 생성해주고 아래 watchlist를 업데이트!
        userprofile_id = UserProfileModel.objects.filter(user=instance).update(**userprofile)
        userprofile = UserProfileModel.objects.get(id=userprofile_id)
        
        # set함수는 언패킹을 하지 않고, 리스트 형태의 파라미터를 받아 수정 가능!
        userprofile.watchlist.set(get_watchlist)
        userprofile.save()

        return instance


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


class ProductSerializer(serializers.ModelSerializer):
    category = WatchListSerializer(read_only=True, many=True)
    
    class Meta:
        model = ProductModel

        fields = ["title", "content", "thumbnail", "category", "like_cnt"]