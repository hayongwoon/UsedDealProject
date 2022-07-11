from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from product.serializers import ProductSerializer
from product.models import Product as ProductModel
from core.permissions import IsRegisterdMoreThanTwoRliabilityPoint


# Create your views here.
class ProductApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        active_products = ProductModel.objects.filter(is_active=True).order_by('-register_date')
        return Response(ProductSerializer(active_products, many=True).data, status=status.HTTP_200_OK)


class SingleProductApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]

    def get(self, request, obj_id):
        try:
            product = ProductModel.objects.get(id=obj_id)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        except ProductModel.DoesNotExist:
            return Response({"msg": "존재하지 않는 상품 입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        try:
            product = ProductModel.objects.get(id=obj_id)
            serializer = ProductSerializer(product, data=request.data ,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            
        except ProductModel.DoesNotExist:
            return Response({"msg": "존재하지 않는 상품 입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, obj_id):
        try:
            product = ProductModel.objects.get(id=obj_id)
            product.delete()
            return Response({"message":"상품이 삭제되었습니다."})

        except ProductModel.DoesNotExist:
            return Response({"message":"이미 삭제 된 상품입니다."})


