from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login',views.user_login,name='login'),
    path('signup',views.user_signup,name='signup'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('cart',views.cart,name='cart'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('add_address',views.add_address,name='add_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),    
    path('edit_address/<int:id>',views.edit_address,name='edit_address'),    
    path('profile_edit',views.profile_edit,name='profile_edit'),    
    path('user_shop',views.user_shop,name='user_shop'), 
    path('checkout',views.checkout,name='checkout'),   
    path('wishlist',views.wishlistview,name='wishlist'),
    path('wishlistadd/<int:id>',views.wishlistadd,name='wishlistadd'),
    path('deletewishlistitem/<int:id>',views.wishlistitemdelete,name='deletewishlistitem'),
    path('product/<int:id>', views.product_details, name='userproduct'),
    path('cartadd',views.cartadd,name='cartadd'),
    path('categoryfilter/<str:value>',views.selectedView,name='categoryfilter'),
    path('deletecartitem/<int:item_id>/',views.deleteFromCart,name='deletecartitem'),
]
