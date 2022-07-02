from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class CreateProductCommentApiView(APIView):
    # 댓글 생성
    def post(self, request):
        return Response({"msg":"post good!"})


class ProductAllCommentsApiView(APIView):
    # 해당 상품의 달린 모든 댓글 보기
    def get(self, request, product_id):
        return Response({"msg":"해당 상품의 달린 모든 댓글"})


class SingleProductCommentApiView(APIView):
    # 단일 댓글 조회
    def get(self, request, obj_id):
        return Response({"msg":"get good!"})

    # 댓글 수정
    def put(self, request, obj_id):
        return Response({"msg":"put good!"})

    # 댓글 삭제
    def delete(self, request, obj_id):
        return Response({"msg":"delete good!"})