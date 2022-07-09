from dataclasses import field
from django.urls import is_valid_path
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import WatchList as WatchListModel
from product.models import Product as ProductModel
from product_like.models import Like as LikeModel
from success_deal.models import SuccessDeal as SuccessDealModel


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

        user.set_password(validated_data['password'])
        user.save()

        userprofile = UserProfileModel.objects.create(user=user, **userprofile)
        userprofile.watchlist.add(*get_watchlist)
        userprofile.save()

        return user

    def update(self, instance, validated_data):
        userprofile = validated_data.pop('userprofile')
        get_watchlist = userprofile.pop('get_watchlist', [])

        # 유저 객체 수정
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save() 

        # 유저 프로필 객체 수정
        profile = instance.userprofile
        for key, value in userprofile.items():
            setattr(profile, key, value)

        profile.save()

        # 유저 프로필의 관심목록 수정
        profile.watchlist.set(get_watchlist)
        profile.save()

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

        fields = ["title", "content", "thumbnail", "category", "like_cnt", "is_active"]


class LikedProductByUserSerialzer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = LikeModel

        fields = ["product"]


class PurchasedProductByUserSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = SuccessDealModel

        fields = ["product"]