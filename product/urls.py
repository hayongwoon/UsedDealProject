from django.urls import path

from product.views import ProductApiView, SingleProductApiView, SellingListApiView


urlpatterns = [
    # 상품 등록 및 모든 상품 조회(최신순) 뷰
    path('', ProductApiView.as_view()),
    
    # 사용자 판매 목록 뷰
    path('<user_id>/sellinglist/', SellingListApiView.as_view()),

    # 단일 상품 뷰
    path('<obj_id>/', SingleProductApiView.as_view()),
    

]
