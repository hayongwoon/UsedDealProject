from django.db import models

from user.models import User as UserModel
from product.models import Product as ProductModel

# Create your models here.
class SuccessDeal(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductModel, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    review = models.TextField("구매 후기")
    created = models.DateTimeField("등록시간", auto_now_add=True)
    rating = models.IntegerField("평점")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_user_product_review"),
        ]