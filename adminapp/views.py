from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import Accounts
from django.db.models import Q
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
    if 'admin_id' in request.session:
        item = Product.objects.filter(product_status=True).order_by("id")
        return render(request, 'admin/Product_management.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)
    
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
    if 'admin_id' in request.session:
        if 'search' in request.GET:
            sh = request.GET['search']
            multiple_sh = Q(Q(first_name__icontains=sh) | Q(email__contains=sh))
            item = Accounts.objects.filter(multiple_sh).order_by("-id")
            return render(request, 'users.html',{'data':item})
        else:
            item = Accounts.objects.all().order_by("-id")
            return render(request, 'admin/user_mangement.html',{'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)
    

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


def add_category(request):
    if 'admin_id' in request.session:
        if request.method =='POST':
                category_name = str(request.POST['c_name'])
                category_name = category_name.upper()
                description   = request.POST['desc']
                if Category.objects.filter(category_name = category_name):
                    messages.error(request,"category alredy exists",extra_tags='categoryerror')
                    return redirect(add_category)
                elif category_name == "" or description =="":
                    messages.error(request,"enter values")
                else:
                    item = Category.objects.create(
                        category_name = category_name,
                        description = description
                    )
                    return redirect(catogary_mangement)
                    
    return render(request,'admin/add_category.html')

def category_delete(request, id):
    item = Category.objects.filter(id=id)
    item.delete()
    
    return redirect(catogary_mangement)

def category_edit(request, id):
    if 'admin_id' in request.session:
        item=Category.objects.get(id=id)
        if request.method == 'POST':
            if Category.objects.filter(category_name = request.POST['category_name']) and request.POST['category_name']!= item.category_name:
                messages.error(request,'Category already exists!!',extra_tags='categoryerror')
                return render(request, 'admin/categoryedit.html', {'data':item})
            elif request.POST['category_name'] == '' or request.POST['description'] == '':
                messages.error(request,'Categoryname must not be empty!!', extra_tags='categoryerror')
                return render(request, 'admin/categoryedit.html', {'data':item})
            else:
                item.category_name = request.POST['category_name']
                item.description = request.POST['description']
                item.save()
                return redirect(catogary_mangement)
        else:
            return render(request, 'admin/categoryedit.html', {'data':item})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)


def product_delete(request, id):
    if 'admin_id' in request.session:
        item = Product.objects.filter(id = id)
        item.delete()
        return redirect(product_management)


def product_edit(request,id):
    if 'admin_id' in request.session:
        item = Product.objects.get(id = id)
        value =Category.objects.all()
        if request.method == 'POST':
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']
            category_name = request.POST['category']
            brand = request.POST['brand']
            try:
                image = request.FILES['uploadFromPC']
                image1 = request.FILES['uploadFromPC1']
                image2 = request.FILES['uploadFromPC2']
            except:
                print('please add an image!!')
            if  brand=='':
                messages.error(request,'All fields are required')
                return redirect('/admin/edit_product/'+str(id))
            if product_name == '' or description =='' or price=='' or stock==''or category_name == '' or brand=='':
                messages.error(request,'All fields are required', extra_tags='productadderror')
                return redirect('/admin/edit_product/'+str(id))
            elif int(price)<0 or int(stock)<0:
                messages.error(request,'Negative number is not supportted for price and stock', extra_tags='productadderror')
                return redirect('/admin/edit_product/'+str(id))
            item.product_name = request.POST['product_name']
            item.description = request.POST['description']
            item.price = request.POST['price']
            item.stock = request.POST['stock']
            c_name = Category.objects.get(category_name = request.POST['category'])
            item.category = c_name
            item.brand = request.POST['brand']
            item.product_status = request.POST['product_status']
            try:       
                item.image = request.FILES['uploadFromPC']
                item.image1 = request.FILES['uploadFromPC1']
                item.image2 = request.FILES['uploadFromPC2']
            except:
                print('sdsdffdfdf')
                
            item.save()
            return redirect(product_management)
        return render(request, 'admin/productedit.html',{'data':item, 'value':value})
    else:
        messages.error(request, 'Only admin can access')
        return redirect(admin_login)



def blockuser(request,id):
    item = Accounts.objects.get(id = id)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True
    item.save()
    return redirect(user_mangement)
