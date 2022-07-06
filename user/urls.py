from django.urls import path

from user.views import CreateUserApiView, UserLoginView, UserSellingListApiView, UserProfileApiVeiw, UserPurchaseListApiView, UserLikeListApiView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    # 회원가입 - signup/ -> post
    path('signup/', CreateUserApiView.as_view()),

    # 로그인 -> post
    path('login/', UserLoginView.as_view()),

    # 로그아웃 - logout/ -> post

    # 프로필 - <user_id>/profile/  -> put, get, delete
    path('<user_id>/profile/', UserProfileApiVeiw.as_view()),

    # 좋아요한 리스트 - <user_id>/likelist/  -> get
    path('<user_id>/likelist/', UserLikeListApiView.as_view()),

    # 판매 리스트 -> get
    path('<user_id>/sellinglist/', UserSellingListApiView.as_view()),

    # 구매 리스트 -> <user_id>/purchaselist/  -> get
    path('<user_id>/purchaselist/', UserPurchaseListApiView.as_view()),

    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
