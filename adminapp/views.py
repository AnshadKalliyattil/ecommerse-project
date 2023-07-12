from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import Accounts


# Create your views here.
def index(request):
    return render(request,'admin/adminindex.html')
def admin_login(request):
    
    if 'admin_id' in request.session:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        if username == '' and password == '':
            messages.error(request, 'Please enter the values!!!')
            return redirect(admin_login)
        elif username != 'admin':
            messages.error(request, 'Only admin can access!!!')
            return redirect(admin_login)
        elif Accounts.objects.filter(username = username):
            admin = authenticate(username = username, password = password)
            if admin is not None:
                request.session['admin_id'] = username
                login(request,admin)
                return redirect(index)
            else:
                messages.error(request, 'Invalid Credentials!!!')
                return redirect(admin_login)
        else:
            messages.error(request, 'Admin Credentials is invalid!!!')
            return redirect(admin_login)
        
        return redirect (index)
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