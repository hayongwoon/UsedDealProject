from django.urls import path

from success_deal.views import SuccessDealApiView

urlpatterns = [
    path('', SuccessDealApiView.as_view()),
   
]