from django.urls import path

from success_deal.views import SuccessDealApiView

urlpatterns = [
    path('<product_id>/', SuccessDealApiView.as_view()),
   
]