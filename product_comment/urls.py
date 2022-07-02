from django.urls import path

from product_comment.views import CreateProductCommentApiView, ProductAllCommentsApiView, SingleProductCommentApiView

urlpatterns = [
    # 댓글 생성 뷰
    path('', CreateProductCommentApiView.as_view()),

    # 해당 상품의 모든 댓글
    path('<product_id>/comments/', ProductAllCommentsApiView.as_view()),

    # 단일 댓글 뷰
    path('<obj_id>/', SingleProductCommentApiView.as_view()),
   
]