from rest_framework import serializers

from success_deal.models import SuccessDeal as SuccessDealModel
from product.models import Product as ProductModel
from user.models import User as UserModel 


class SuccessDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessDealModel

        fields = ["user", "review", "rating"]

    def create(self, validated_data):
        success_deal = SuccessDealModel(**validated_data)
        # comment.user = self.context['request'].user
        success_deal.user = UserModel.objects.get(id=3) # test user
        success_deal.product = ProductModel.objects.get(id=self.context['product_id'])

        success_deal.save()

        return success_deal