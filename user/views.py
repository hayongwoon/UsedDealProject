from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from user import serializers

from user.serializers import UserSerializer, UserLoginSerializer
from user.models import User as UserModel


# Create your views here.
class UserApiView(APIView):
    #회원 가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    #회원 정보
    def get(self, request):
        # user = request.user
        user = UserModel.objects.get(id=1) #test user
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    #회원 정보 수정
    def put(self, request):
        return Response({'msg':'put success'})

    #회원 탈퇴 - 계정 비활성화
    def delete(self, request):
        return Response({'msg':'delete success'})


class UserLoginView(APIView):
    #로그인
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['username'] == "None": # username required
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': True,
            'token': serializer.data['token'] # 시리얼라이저에서 받은 토큰 전달
        }
        return Response(response, status=status.HTTP_200_OK)