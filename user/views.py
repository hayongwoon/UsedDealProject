from django.shortcuts import render
from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
#회원 가입 post
#로그아웃 
#다른 회원 정보
#로그인 한 사용자의 구매 목록 get
#로그인 한 사용자의 판매 목록 get
class UserApiView(APIView):
    #로그인
    def post(self, request):
        return Response({'msg':'post success'})

    #나의 정보
    def get(self, request):
        return Response({'msg':'get success'})

    #회원 정보 수정
    def put(self, request):
        return Response({'msg':'put success'})

    #계정 비활성화
    def delete(self, request):
        return Response({'msg':'delete success'})

