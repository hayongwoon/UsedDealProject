from atexit import register
from unicodedata import category
from product.models import Product as ProductModel
from user.models import User as UserModel, WatchList as WatchListModel

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel

        fields = ["username", "phone", "deal_reliability_avg"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListModel

        fields = ["name"]


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer(read_only=True)
    get_categorylist = serializers.ListField(write_only=True, many=True)
    register_date = serializers.DateTimeField(auto_now_add=True)
    
    class Meta:
        model = ProductModel

        fields = ["user", "title", "content", "thumbnail", "category", "get_categorylist", "like_cnt", "register_date"]
        read_only_fields = ['like_cnt']