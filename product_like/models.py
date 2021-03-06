from django.db import models

from user.models import User as UserModel
from product.models import Product as ProductModel

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(to=UserModel, related_name="like_user",on_delete=models.CASCADE)
    product = models.ForeignKey(to=ProductModel, related_name="like_product", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_user_product"),
        ]