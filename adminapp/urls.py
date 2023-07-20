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
    path('add_category',views.add_category,name='add_category'),  
    path('deletecategory/<int:id>',views.category_delete,name='deletecategory'),  
    path('editcategory/<int:id>', views.category_edit, name='editcategory'),
    path('edit_product/<int:id>',views.product_edit,name='edit_product'),
    path('deleteproduct/<int:id>', views.product_delete, name='deleteproduct'),
    path('user_mangement/', views.user_mangement, name='user_mangement'),
    path('blockuser/<int:id>', views.blockuser, name='blockuser'),
]
