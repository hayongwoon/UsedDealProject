from django.urls import path

from product.views import ProductApiView, SingleProductApiView, SellingListApiView


urlpatterns = [
    path('', ProductApiView.as_view()),
    
    # 사용자 판매 목록 뷰
    path('<user_id>/sellinglist/', SellingListApiView.as_view()),

    # 단일 상품 뷰
    path('<obj_id>/', SingleProductApiView.as_view()),
    

]
