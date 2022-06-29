from django.urls import path
from user import views
from user.views import UserApiView, signup


urlpatterns = [
    path('', UserApiView.as_view()),
    path('signup/', views.signup, name='signup'),
]