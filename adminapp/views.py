from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'admin/adminindex.html')
def admin_login(request):
    return render(request,'admin/adminlogin.html')
def product_management(request):
    return render(request,'admin/Product_management.html')
def catogary_mangement(request):
    return render(request,'admin/catogary_mangement.html')
def coupen_mangement(request):
    return render(request,'admin/coupen_mangement.html')
def offer_mangement(request):
    return render(request,'admin/offer_mangement.html')
def sales_report(request):
    return render(request,'admin/sales_report.html')
def order_mangement(request):
    return render(request,'admin/order_mangement.html')
def user_mangement(request):
    return render(request,'admin/user_mangement.html')
def add_product(request):
    return render(request,'admin/add_product.html')