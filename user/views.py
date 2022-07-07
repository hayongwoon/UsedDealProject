from django.shortcuts import render

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from success_deal.models import SuccessDeal as SuccessDealModel

from user.serializers import UserSerializer, UserLoginSerializer, ProductSerializer, LikedProductByUserSerialzer, PurchasedProductByUserSerializer
from user.models import User as UserModel

from product.models import Product as ProductModel
from product_like.models import Like as LikeModel


# Create your views here.
class CreateUserApiView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['username'] == "None":
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': True,
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


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
   

class UserProfileApiVeiw(APIView):    
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

    def put(self, request, user_id):
        user = request.user
        print(user)
        if user.is_anonymous:
            return Response({"error": "로그인 후 수정 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.id == int(user_id): 
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"msg":"사용자 본인만 수정이 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = request.user
        if user.id == int(user_id):
            UserModel.objects.filter(id=user.id).update(is_active=False)
            return Response({'msg':'계정이 삭제 되었습니다.'})


class UserSellingListApiView(APIView):
    def get(self, request, user_id):
        selling_products = ProductModel.objects.filter(user=user_id, is_active=True).order_by('-register_date') 
        return Response(ProductSerializer(selling_products, many=True).data, status=status.HTTP_200_OK)


class UserPurchaseListApiView(APIView):
    def get(self, request, user_id):
        purchased_products = SuccessDealModel.objects.filter(buyer=user_id).order_by('-created')
        return Response(PurchasedProductByUserSerializer(purchased_products, many=True).data, status=status.HTTP_200_OK)


class UserLikeListApiView(APIView):
    def get(self, request, user_id):
        liked_products = LikeModel.objects.filter(user=user_id).order_by('-created')
        return Response(LikedProductByUserSerialzer(liked_products, many=True).data, status=status.HTTP_200_OK)
        