from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class ProductApiView(APIView):
    # 상품 등록
    def post(self, request):
        return Response({"msg":"post success"})

    # 모든 상품 조회(등록 순)
    def get(self, request):
        return Response({"msg":"get success"})

    # 등록한 상품 수정
    def put(self, request):
        return Response({"msg":"put success"})

    # 상품 삭제(비활성화)
    def delete(self, request):
        return Response({"msg":"delete success"})