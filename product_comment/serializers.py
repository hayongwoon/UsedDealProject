from multiprocessing import context
from rest_framework import serializers

from product_comment.models import Comment as CommentModel
from product.models import Product as ProductModel
from user.models import User as UserModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel

        fields = ["article", "user", "content"]

    def create(self, validated_data):
        comment = CommentModel(**validated_data)
        # comment.user = self.context['request'].user
        comment.user = UserModel.objects.get(id=3)
        comment.article = ProductModel.objects.get(id=self.context['product_id'])

        comment.save()

        return comment



        