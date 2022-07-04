from multiprocessing import context
from rest_framework import serializers

from product_comment.models import Comment as CommentModel
from product.models import Product as ProductModel
from user.models import User as UserModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel

        fields = ["user", "content", "created"]
        read_only_fields = ['created']


    def create(self, validated_data):
        comment = CommentModel(**validated_data)
        # comment.user = self.context['request'].user
        comment.user = UserModel.objects.get(id=3) # test user
        comment.article = ProductModel.objects.get(id=self.context['product_id'])

        comment.save()

        return comment

    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data)
    

class ProductCommentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    def get_comments(self, obj):
        comments = obj.comment_article
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = ProductModel

        fields = ["user", "title", "content", "thumbnail", "category", "like_cnt", "comments"]
        