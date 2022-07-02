from django.urls import path

from product_comment.views import ProductCommentApiView, SingleProductCommentApiView, SingleProductCommentApiView

urlpatterns = [
    # 댓글 생성 뷰, 해당 상품의 모든 댓글
    path('<product_id>/comments/', ProductCommentApiView.as_view()),

    # 단일 댓글 뷰
    path('<obj_id>/', SingleProductCommentApiView.as_view()),
   
]