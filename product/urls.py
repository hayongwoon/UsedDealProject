from django.urls import path

from product.views import ProductApiView


urlpatterns = [
    path('', ProductApiView.as_view()),

]
