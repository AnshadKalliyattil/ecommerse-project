from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index),
    path('login',views.user_login,name='login'),
    path('signup',views.user_signup,name='signup'),
    path('user_cartsignup',views.user_cart,name='user_cart'),
    path('user_profile',views.user_profile,name='user_profile'),
]
