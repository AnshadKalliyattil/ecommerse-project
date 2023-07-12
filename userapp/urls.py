from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login',views.user_login,name='login'),
    path('signup',views.user_signup,name='signup'),
    path('user_cartsignup',views.user_cart,name='user_cart'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('order',views.order,name='order'),
    path('forgot',views.forgot_password,name='forgot'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('add_address',views.add_address,name='add_address')
]
