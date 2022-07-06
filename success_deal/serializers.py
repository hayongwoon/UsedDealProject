from rest_framework import serializers

from success_deal.models import SuccessDeal as SuccessDealModel
from product.models import Product as ProductModel
from user.models import User as UserModel 


class SuccessDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessDealModel

        fields = ["buyer", "review", "rating"]

    def create(self, validated_data):
        success_deal = SuccessDealModel(**validated_data)
        # comment.user = self.context['request'].user
        success_deal.buyer = UserModel.objects.get(id=5) # test user

        seller_id = ProductModel.objects.get(id=self.context['product_id']).user.id
        success_deal.seller = UserModel.objects.get(id=seller_id)
        success_deal.product = ProductModel.objects.get(id=self.context['product_id'])

        success_deal.save()

        ProductModel.objects.filter(id=self.context['product_id']).update(is_active=False)

        return success_deal