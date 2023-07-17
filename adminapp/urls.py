from django.urls import include,path
from . import views

urlpatterns = [
    path('admin_dashboard', views.index,name='admin_dashboard'),
    path('',views.admin_login,name='adminlogin'),
    path('product_management',views.product_management,name='product_management'),
    path('catogary_mangement',views.catogary_mangement,name='catogary_mangement'), 
    path('coupen_mangement',views.coupen_mangement,name='coupen_mangement'),
    path('offer_mangement',views.offer_mangement,name='offer_mangement'), 
    path('sales_report',views.sales_report,name='sales_report'), 
    path('order_mangemen',views.order_mangement,name='order_mangemen'),
    path('user_mangement',views. user_mangement,name=' user_mangement'),   
    path('add_product',views.add_product,name='add_product'),   
    path('admin_logout',views.admin_logout,name='admin_logout'),  
]
