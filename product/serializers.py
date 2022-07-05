from atexit import register
from unicodedata import category
from product.models import Product as ProductModel
from user.models import User as UserModel, WatchList as WatchListModel
from product_comment.models import Comment as CommentModel

from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel

        fields = ["user", "content", "created"] 


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
    category = CategorySerializer(read_only=True, many=True)
    get_categorylist = serializers.ListField(write_only=True)
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        comments = obj.comment_article
        return CommentSerializer(comments, many=True).data
    
    class Meta:
        model = ProductModel

        fields = ["user", "title", "content", "thumbnail", "category", "get_categorylist", "like_cnt", "comments"]
        read_only_fields = ['like_cnt']

    def create(self, validated_data):
        get_categorylist = validated_data.pop("get_categorylist", [])

        # product 객체 생성
        product = ProductModel(**validated_data)
        # product.user = self.context["request"].user
        product.user = UserModel.objects.get(id=16) #test user
        product.save()

        product.category.add(*get_categorylist)
        product.save()

        return product

    def update(self, instance, validated_data):
        get_categorylist = validated_data.pop("get_categorylist", [])

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        instance.category.set(get_categorylist)

        return instance