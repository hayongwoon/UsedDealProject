from django.urls import path, include

from product.views import ProductApiView, SingleProductApiView


urlpatterns = [
    # 상품 등록 및 모든 상품 조회(최신순) 뷰
    path('', ProductApiView.as_view()),

    # 단일 상품 - 조회, 수정, 삭제
    path('<obj_id>/', SingleProductApiView.as_view()),
    
    # 상품의 댓글
    path('<product_id>/comments/', include('product_comment.urls')),

    # 상품의 좋아요
    path('<product_id>/like/', include('product_like.urls')), 

    # 상품의 거래 완료
    path('<product_id>/deal/', include('success_deal.urls')),

]
