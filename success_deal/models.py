from django.db import models

from user.models import User as UserModel
from product.models import Product as ProductModel

# Create your models here.
class SuccessDeal(models.Model):
    buyer = models.ForeignKey(UserModel, related_name='deal_buyer', verbose_name="구매자", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(UserModel, related_name='deal_seller', verbose_name="판매자", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductModel, related_name='deal_product', verbose_name='상품', on_delete=models.SET_NULL, null=True)
    review = models.TextField("구매 후기")
    created = models.DateTimeField("등록시간", auto_now_add=True)
    rating = models.IntegerField("평점")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["buyer", "product"], name="unique_user_product_review"),
        ]