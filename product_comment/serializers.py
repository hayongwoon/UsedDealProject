from rest_framework import serializers

from product_comment.models import Comment as CommentModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel

        fields = ["article", "user", "content"]

        