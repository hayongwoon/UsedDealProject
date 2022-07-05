from django.urls import path

from product_like.views import LikeApiView

urlpatterns = [
    path('<product_id>/', LikeApiView.as_view()),
   
]