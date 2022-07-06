from django.urls import path

from product_comment.views import ProductCommentApiView, SingleProductCommentApiView, SingleProductCommentApiView

urlpatterns = [
    # 댓글 생성 뷰, 해당 상품의 모든 댓글
    path('', ProductCommentApiView.as_view()),

    # 단일 댓글 - 조회, 수정, 삭제
    path('<obj_id>/', SingleProductCommentApiView.as_view()),
   
]