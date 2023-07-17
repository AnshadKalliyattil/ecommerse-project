from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import Accounts
from productapp.models import Category,Product


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
    return render(request,'admin/adminlogin.html')

def product_management(request):
    return render(request,'admin/Product_management.html')

def catogary_mangement(request):
      if 'admin_id' in request.session:
        item = Category.objects.all()
        return render(request, 'admin/Catogary_Management.html', {'data':item})
      else:
        messages.error(request, 'Only admin can access')
      return redirect(admin_login)

    
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
    if 'admin_id' in request.session:
        value = Category.objects.all()
        context = {
            'value' : value
        }
        if request.method == 'POST':
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']
            category_name = request.POST['category']
            brand = request.POST['brand']
            image=image1=image2=''
            try:
                image = request.FILES['uploadFromPC']
                image1 = request.FILES['uploadFromPC1']
                image2 = request.FILES['uploadFromPC2']
            except:
                print('please add an image!!')

            print(price)
            
            if product_name == '' or description =='' or price=='' or stock==''or category_name == '' or brand=='' or image=='' or image1=='' or image2 == '':
                messages.error(request,'All fields are required', extra_tags='productadderror')
                return redirect(add_product)
            elif int(price)<0 or int(stock)<0:
                messages.error(request,'Negative number is not supportted for price and stock', extra_tags='productadderror')
                return redirect(add_product)
            elif category_name == 'Select One':
                messages.error(request,'Please select a category', extra_tags='productadderror')
                return redirect(add_product)
            
            if image == None:
                return redirect(add_product)
            product_status = request.POST['product_status']
            item = Product.objects.create(
                product_name=product_name,
                description=description,
                price=price,
                stock=stock,
                brand=brand,
                image=image,
                image1=image1,
                image2=image2,
                product_status=product_status
            )
            item.category = Category.objects.get(category_name=category_name)
            item.save()
            return redirect(product_management)
        return render(request, 'admin/add_product.html', context)
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)    
 

   
def admin_logout(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
        admin_login(request)
        return redirect(admin_login)
    return render(request,'user/adminlogin.html')