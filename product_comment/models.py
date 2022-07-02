from django.db import models
from product.models import Product as ProductModel
from user.models import User as UserModel

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(ProductModel, verbose_name='댓글', related_name='comment_article', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, verbose_name='작성자', related_name='comment_user', on_delete=models.CASCADE)
    content = models.TextField('내용')

    def __str__(self):
        return f'{self.user}님의 댓글입니다.'