from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Product as ProductModel
from success_deal.serializers import SuccessDealSerializer

# Create your views here.
class SuccessDealApiView(APIView):
    # 판매 완료 -> 구매후기 생성
    def post(self, request, product_id):
        serializer = SuccessDealSerializer(data=request.data, context={'request': request, 'product_id': product_id}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)