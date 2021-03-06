from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from product_comment.serializers import CommentSerializer, ProductCommentSerializer

from user.models import User as UserModel
from product.models import Product as ProductModel
from product_comment.models import Comment as CommentModel
from core.permissions import IsRegisterdMoreThanTwoRliabilityPoint


# Create your views here.
class ProductCommentApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]

    # 댓글 생성
    def post(self, request, product_id):
        serializer = CommentSerializer(data=request.data, context={'request':request, 'product_id':product_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # 해당 상품의 달린 모든 댓글 보기
    def get(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
            serializer = ProductCommentSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ProductModel.DoesNotExist:
            return Response({"msg":"게시글이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class SingleProductCommentApiView(APIView):
    permission_classes = [IsRegisterdMoreThanTwoRliabilityPoint]

    # 단일 댓글 조회
    def get(self, request, product_id, obj_id):
        try:
            comment = CommentModel.objects.get(id=obj_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CommentModel.DoesNotExist:
            return Response({"msg":"해당 댓글은 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 수정
    def put(self, request, product_id, obj_id):
        try:
            comment = CommentModel.objects.get(id=obj_id)
            serializer = CommentSerializer(comment, data=request.data,  partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

        except CommentModel.DoesNotExist:
            return Response({'msg':'존재하지 않는 댓글입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, product_id, obj_id):
        try:
            CommentModel.objects.get(id=obj_id).delete()
            return Response({"msg":"댓글이 삭제되었습니다."})
            
        except CommentModel.DoesNotExist:
            return Response({"msg":"이미 삭제 된 댓글입니다."}, status=status.HTTP_400_BAD_REQUEST)

        