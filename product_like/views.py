from django.shortcuts import render
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response

from product_like.models import Like as LikeModel
from product.models import Product as ProductModel

# Create your views here.
class LikeApiView(APIView):
    # 좋아요 생성 
    def post(self, request, product_id):
        LikeModel.objects.create(user_id=16, product_id=product_id)
        ProductModel.objects.filter(id=product_id).update(like_cnt=F("like_cnt") + 1)

        return Response({"msg":"좋아요"})

    # 좋아요 취소
    def delete(self, request, product_id):
        delete_cnt, _ = LikeModel.objects.filter(user_id=16, product_id=product_id).delete()
        if delete_cnt: # 좋아요 수가 0보다 클 때
            ProductModel.objects.filter(id=product_id).update(like_cnt=F("like_cnt") - 1)
            return Response({"msg":"좋아요 취소"})