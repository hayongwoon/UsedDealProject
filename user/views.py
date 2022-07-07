from functools import partial
from lib2to3.pgen2 import token
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, authenticate

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, UserLoginSerializer, ProductSerializer
from user.models import User as UserModel

from product.models import Product as ProductModel
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import permission_classes


# Create your views here.
class CreateUserApiView(APIView):
    #회원 가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginApiView(APIView):
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


@permission_classes([IsAuthenticated])
class UserLogoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})
   

@permission_classes([IsAuthenticated])
class UserProfileApiVeiw(APIView):    
    #회원 정보
    def get(self, request, user_id):
        print(request.user)
        try:
            user = UserModel.objects.get(id=user_id)
            if user.is_active:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"msg":"비활성화 계정입니다."})

        except UserModel.DoesNotExist:
            return Response({"msg":"존재하지 않는 회원입니다."})

    #회원 정보 수정
    def put(self, request, user_id):
        user = request.user
        print(user)
        if user.is_anonymous:
            return Response({"error": "로그인 후 수정 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 로그인 한 사용자가 본인 프로필 수정을 할 때만 가능
        if user.id == int(user_id): 
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"msg":"사용자 본인만 수정이 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

    #회원 탈퇴 - 계정 비활성화
    def delete(self, request, user_id):
        # 로그인 확인 후 처리
        user = request.user
        if user.id == int(user_id):
        # user = UserModel.objects.get(id=user_id) #test user
            UserModel.objects.filter(id=user.id).update(is_active=False) #test user
            return Response({'msg':'계정이 삭제 되었습니다.'})


# 사용자의 판매 목록
class UserSellingListApiView(APIView):
    def get(self, request, user_id):
        user_products = ProductModel.objects.filter(user=user_id).order_by('-register_date') 
        return Response(ProductSerializer(user_products, many=True).data, status=status.HTTP_200_OK)


# 사용자의 구매 목록
class UserPurchaseListApiView(APIView):
    def get(self, request, user_id):
        return Response({"msg":"사용자 구매 목록 조회"})


# 사용자의 좋아요 목록
class UserLikeListApiView(APIView):
    def get(self, request, user_id):
        print(request.user)
        return Response({"msg":"사용자 좋아요 목록 조회"})