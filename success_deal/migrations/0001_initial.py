# Generated by Django 4.0.5 on 2022-07-05 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessDeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(verbose_name='구매 후기')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('rating', models.IntegerField(verbose_name='평점')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product', verbose_name='상품')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.AddConstraint(
            model_name='successdeal',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product_review'),
        ),
    ]