from django.urls import path

from product.views import ProductApiView, SingleProductApiView


urlpatterns = [
    path('', ProductApiView.as_view()),
    path('<obj_id>/', SingleProductApiView.as_view()),

]
