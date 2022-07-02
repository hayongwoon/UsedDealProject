from functools import partial
from multiprocessing import context
from django.shortcuts import render
import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import BasePermission

from product.serializers import ProductSerializer
from product.models import Product as ProductModel


class IsRegisterdMoreThanTwoRliabilityPoint(BasePermission):
    """
    거래 신뢰도가 2 보다 높은 사용자는 쓰기, 수정, 삭제 가능
    이외에는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if request.method in self.SAFE_METHODS or \
            user.is_authenticated and request.user.deal_reliability_avg > 2:

            return True

        return False

# Create your views here.
class ProductApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]
    # 상품 등록
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # 모든 상품 조회(등록 순, 팔고있는is_active=True)
    def get(self, request):
        products = ProductModel.objects.filter(is_active=True).order_by('-register_date')
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)


class SingleProductApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]
    # 단일 상품 조회
    def get(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    # 등록한 상품 수정
    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        serializer = ProductSerializer(product, data=request.data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # 상품 삭제
    def delete(self, request, obj_id):
        try:
            ProductModel.objects.get(id=obj_id).delete()
            return Response({"message":"상품이 삭제되었습니다."})
        except:
            return Response({"message":"이미 삭제 된 상품입니다."})

# 사용자의 판매 목록