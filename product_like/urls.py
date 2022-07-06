from django.urls import path

from product_like.views import LikeApiView

urlpatterns = [
    path('', LikeApiView.as_view()),
   
]