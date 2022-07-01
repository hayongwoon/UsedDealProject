from unicodedata import category
from django.db import models

from user.models import WatchList as WatchListModel
from user.models import User as UserModel

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(to=UserModel, related_name='product_user', on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용", max_length=500)
    thumbnail = models.ImageField('섬네일', upload_to='product/thumbnail',  height_field=None, width_field=None, max_length=None)
    category = models.ManyToManyField(to=WatchListModel, related_name='product_category')

    like_cnt = models.IntegerField('좋아요 수', default=0)
    register_date = models.DateTimeField("등록일", auto_now_add=True)
    is_active = models.BooleanField("활성화 여부", default=True)

    def __str__(self):
        return f'판매자: {self.user}, 제목: {self.title}, 분류: {self.category}'
