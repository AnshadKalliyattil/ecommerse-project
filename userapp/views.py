from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect, render
from accounts .models import Accounts,CustomerAdress
from django.contrib.auth import authenticate
from productapp .models import Category,Product
from cartapp .models import CartItem,Order,MyWishList

# Create your views here.
def index(request):
 
    return render(request,'user/index.html')

def user_login(request):
    if 'user_id' in request.session:
         return redirect(index)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        if username == '' and password == '':
            messages.error(request, 'Please enter the values!!!')
            return redirect(user_login)
        elif Accounts.objects.filter(username = username):
            data = Accounts.objects.get(username = username)
            if data.is_active == False :
                messages.error(request, 'Your account got blocked!!!')
                return redirect(user_login)
            user = authenticate(username = username, password = password)
            if user is not None:
                request.session['user_id']=username
                return redirect(index)
            else:
               messages.error(request, 'Invalid Credentials!!!')
               return redirect(user_login)
        else:
               messages.error(request, 'user not exist!!!')
               return redirect(user_login)
    return render(request,'user/login.html')
   
def user_signup(request):  
    if request.method == 'POST':
        username     = request.POST['username']
        first_name   = request.POST['first_name']
        last_name    = request.POST['last_name']
        email        = request.POST['email']
        phone_number = request.POST['phone_number']
        password     = request.POST['pass']
        password1    = request.POST['pass1']

        if password == password1 and len(password)>=6:
            try:
                k=int(request.POST['phone_number'])
            except:
                messages.error(request,'Please enter the phone Number')
                return redirect(user_signup)
            if first_name == '' or last_name == '' or username == '' or email == '' or phone_number == '' or password == '' or password1 == '':
                messages.error(request, 'Firstname must not be empty')
                messages.error(request, 'Lastname must not be empty')
                messages.error(request, 'Username must not be empty')
                messages.error(request, 'Email must not be empty')
                messages.error(request, 'Password must not be empty')
                messages.error(request, 'Phone number must not be empty')
                return redirect(user_signup)
            elif len(phone_number)!=10:
                messages.error(request, 'Enter corrrect phone number')
                return redirect(user_signup)
            elif Accounts.objects.filter(username=username):
                messages.error(request, 'username already  exists')
                return redirect(user_signup)
            elif Accounts.objects.filter(email=email):
                messages.error(request, 'Email already  exists')
                return redirect(user_signup)
            elif Accounts.objects.filter(phone=phone_number):
                messages.error(request, 'Phone number already  exists')
                return redirect(user_signup)
            else:
                if Accounts.objects.filter(username=username):
                    messages.error(request, 'Username already exists')
                    return redirect(user_signup)
                else:
                    item = Accounts.objects.create(
                        first_name =first_name,
                        last_name=last_name,
                        username = username, 
                        email = email,
                        phone = phone_number,
                      
                    )
                    item.set_password(password)
                    item.save()
                    request.session['user_id'] = username
                    return redirect(index)
                
        else:
            messages.error(request, '''Password must be same 
            and must have 6 charecters''')
            return redirect(user_signup)
    return render(request,'user/signup.html')
def user_cart(request):
    return render(request,'user/cart.html')


def user_profile(request):
    if 'user_id' in request.session:
        user    = request.session['user_id']
        user_id = Accounts.objects.get(username=user)
        address = CustomerAdress.objects.filter(user = user_id)
        
        context = {
            'id' : user_id,
            'address' : address
        }
    else:
        context = None
    return render(request,'user/profile.html',context)

def cart(request):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        order_qs = Order.objects.filter(user__username = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(user__username = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        context = {
            'order_object' : order_object
        }
    else:
        user     = request.session.session_key
        order_qs = Order.objects.filter(guest_user = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(guest_user = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        context = {
            'order_object' : order_object
        }
    return render(request,'user/cart.html', context)



def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect(index)
    return render(request,'user/login.html')

def add_address(request):
    if request.method == "POST":
        user         = request.session.get('user_id')
        first_name   = request.POST['first_name']
        last_name    = request.POST['last_name']
        email        = request.POST['email']
        phone_number = request.POST['phone_number']
        house_name   = request.POST['house_name']
        state        = "Kerala"
        country      = "India"
        street_name  = request.POST['street_name']
        city         = request.POST['city']
        post_code    = request.POST['post_code']
        
        item = CustomerAdress.objects.create(
            first_name   = first_name,
            last_name    = last_name,
            email        = email,
            phone_number = phone_number,
            house_name   = house_name,
            state        = state,
            country      = country,
            street_name  = street_name,
            city         = city,
            post_code    = post_code
        )
        
        item.user = Accounts.objects.get(username =user)   
        item.save()
        return redirect(user_profile)   
    return render(request,'user/add_address.html')


def delete_address(request, id):
    item = CustomerAdress.objects.get(id = id)
    item.delete()
    return redirect(user_profile)


def edit_address(request,id):
    item = CustomerAdress.objects.get(id = id)
    if request.method == "POST":
        item.first_name   = request.POST["first_name"]
        item.last_name    = request.POST['last_name']
        item.email        = request.POST['email']
        item.phone_number = request.POST['phone_number']
        item.house_name   = request.POST['house_name']
        item.state        = 'kerala'
        item.country      = 'india'
        item.street_name  = request.POST['street_name']
        item.city         = request.POST['city']
        item.post_code    = request.POST['post_code']
        
        item.save()
        return redirect(user_profile)
    context = {
        'item' : item
    }
    return render(request, 'user/edit_address.html',context)


def profile_edit(request):
        if 'user_id' in request.session:
            user = request.session['user_id']
            item = Accounts.objects.get(username=user)
        
            if request.method =='POST':
                first_name   = request.POST['first_name']
                email        = request.POST['email']
                phone_number = request.POST['phone_number']
                try:
                    k=int(request.POST['phone_number'])
                except:
                    messages.error(request,"please enter a phone number")
                    return redirect(profile_edit)
                if first_name == ''  or email == '' or phone_number =='':
                    messages.error(request,"name must not be empty")
                    messages.error(request,"email must not be empty")
                    messages.error(request,"phone number must not be empty")
                    return redirect (profile_edit)
                elif len(phone_number)!=10:
                    messages.error(request,"please enter a valid number")
                    return redirect(profile_edit)          
                elif Accounts.objects.filter(phone=phone_number) :
                    messages.error(request,"phone number already exists")
                    return redirect(profile_edit)
                elif Accounts.objects.filter(email=email):
                    messages.error(request,"email already exists")
                    return redirect(profile_edit)
                else:
                    item.first_name    = first_name
                    item.phone         = phone_number
                    item.email         = email
                    item.save()
                    return redirect(user_profile)
  
            else:
                return render(request,'user/profile_edit.html', {'data' : item})



def user_shop(request):
    if not request.session.session_key:
        request.session.save()
    if 'user_id' in request.session:
        item     = Product.objects.all().order_by("id")
        category = Category.objects.all()
        user        = Accounts.object.get(username = request.session['user_id'])
        wish        = MyWishList.objects.filter(username = user.id)
        wishlist    = []
        for i in wish:
          wishlist.append(i.product.product_name)
        context     = {
            'data':item,
            'category':category,
            'wishlist':wishlist
        }
    else:
        item     = Product.objects.all().order_by("id")
        wishlist = []
        context   ={
            'data':item,
            'wishlist':wishlist
            
        }
    return render(request,'user/shop.html',context)


def cartadd(request):
    if 'user_id' in request.session:
        product_id   = request.POST.get('product-id')
        quantity     = int(request.POST.get('product-quantity'))
        product_var  = Product.objects.get(id = product_id)
        user         = request.session.get('user_id')
        item         = Accounts.objects.get(username =user)
        id           = item.id
        Order_qs     = Order.objects.filter(user_id = id ,orderd = False)
        if Order_qs.exists():
            order = Order_qs[0]
            if order.items.filter(user_id = id ,product = product_var).exists():
                order_item         =order.items.get(user_id = id, product =product_var)
                order_item.quantity += quantity
                order_item.save()
                return redirect('/product/'+str(product_id))
            else:
                order_item = CartItem.objects.create(user_id=id, product = product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()
                return redirect('/product/'+str(product_id))
            
        else:
            order      = Order.objects.create(user_id=id)
            order_item = CartItem.objects.create(user_id=id, product=product_var, quantity=quantity)
            order.items.add(order_item)
            order.save()
            return redirect('/product/'+str(product_id))
    else:
        product_id   = request.POST.get('product-id')
        quantity     = int(request.POST.get('product-quantity'))
        product_var  = Product.objects.get(id = product_id)
        id           = request.session.session_key
        order_qs     = Order.objects.filter(guest_user= id, orderd = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter( guest_user=id, product=product_var).exists():
                order_item           = order.items.get( guest_user=id, product=product_var)
                order_item.quantity += quantity
                order_item.save()
                return redirect('/product/'+str(product_id))
            else:
                order_item = CartItem.objects.create(guest_user=id, product = product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()       
                return redirect('/product/'+str(product_id))
        else:
            order      = Order.objects.create(guest_user=id)
            order_item = CartItem.objects.create(guest_user=id, product=product_var, quantity=quantity)
            order.items.add(order_item)
            order.save()
            return redirect('/product/'+str(product_id))

    
def wishlistview(request):
    if 'user_id' in request.session:
        user    = Accounts.object.get(username = request.session.get('user_id'))
        item    = MyWishList.objects.filter(username=user.id)
        context = {
            'data':item
        }
        return render(request, 'user/wishlist.html', context)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)
    
    
def wishlistadd(request, id):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        user     = Accounts.object.get(username = user)
        product  = Product.objects.get(id = id)
        if MyWishList.objects.filter(username_id = user.id,product_id = product.id):
            return redirect(user_shop)
        if MyWishList.objects.filter(id=product.id).exists():
            return redirect(user_shop)
        else:
            item = MyWishList.objects.create(username_id = user.id,product_id = product.id )
            return redirect(user_shop)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)


def wishlistitemdelete(request, id):
    if 'user_id' in request.session:
        user     = request.session.get('user_id')
        user     = Accounts.object.get(username = user)
        item     = MyWishList.objects.get(username= user.id,product=id)
        item.delete()
        return redirect(wishlistview)
    else:
        messages.error(request, 'Login is required')
        return redirect(user_login)
        
def product_details(request,id):
    item = Product.objects.get(id = id)
    return render(request, 'user/products.html',{'thisProduct':item})

def cartadd(request):
    if 'user_id' in request.session:
        product_id   = request.POST.get('product-id')
        quantity     = int(request.POST.get('product-quantity'))
        product_var  = Product.objects.get(id = product_id)
        user         = request.session.get('user_id')
        item         = Accounts.objects.get(username = user)
        id           = item.id
        Order_qs     = Order.objects.filter(user_id = id ,orderd = False)
        if Order_qs.exists():
            order = Order_qs[0]
            if order.items.filter(user_id = id ,product = product_var).exists():
                order_item         =order.items.get(user_id = id, product =product_var)
                order_item.quantity += quantity
                order_item.save()
                return redirect('/product/'+str(product_id))
            else:
                order_item = CartItem.objects.create(user_id=id, product = product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()
                return redirect('/product/'+str(product_id))
            
        else:
            order      = Order.objects.create(user_id = id)
            order_item = CartItem.objects.create(user_id=id, product=product_var, quantity=quantity)
            order.items.add(order_item)
            order.save()
            return redirect('/product/'+str(product_id))
    else:
        product_id   = request.POST.get('product-id')
        quantity     = int(request.POST.get('product-quantity'))
        product_var  = Product.objects.get(id = product_id)
        id           = request.session.session_key
        order_qs     = Order.objects.filter(guest_user= id, orderd = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter( guest_user=id, product=product_var).exists():
                order_item           = order.items.get( guest_user=id, product=product_var)
                order_item.quantity += quantity
                order_item.save()
                return redirect('/product/'+str(product_id))
            else:
                order_item = CartItem.objects.create(guest_user=id, product = product_var, quantity=quantity)
                order.items.add(order_item)
                order.save()       
                return redirect('/product/'+str(product_id))
        else:
            order      = Order.objects.create(guest_user=id)
            order_item = CartItem.objects.create(guest_user=id, product=product_var, quantity=quantity)
            order.items.add(order_item)
            order.save()
            return redirect('/product/'+str(product_id))
        
    
def checkout(request):
      if 'user_id' in request.session:
        user    = request.session['user_id']
        user_id = Accounts.objects.get(username = user)
        address = CustomerAdress.objects.filter(user = user_id)
        order_qs = Order.objects.filter(user__username = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(user__username = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        if order_qs.exists():
            order = order_qs[0]
        else:
            order= Order.objects.create(user_id=user_id.id)
        if order_qs.exists():
            orders       = order_qs[0]
            total_amount = float(orders.total_amount_cart)
            tax          = (total_amount) * 3 /100

            
                
            grand_total = float(total_amount) + float(tax)
            grand_total = "{:.1f}".format(grand_total)
            grand_total = float(grand_total)
        else:
            messages.error(request, 'Please add an product',extra_tags='ordererror')
            return render(request,'user/cartempty.html')
        context = {
            'address' : address,
            'order_object' : order_object,
            'order' : order,
            'cart':cart_qs,
            'grand_total' :grand_total,
        }
        
      else:
        user     = request.session.session_key
        address = CustomerAdress.objects.filter(guest_user = user)
        order_qs = Order.objects.filter(guest_user = user, orderd=False).order_by('date_ordered')
        cart_qs  = CartItem.objects.filter(guest_user = user)
        if order_qs.exists() and cart_qs.exists():
            order_object = order_qs[0]
        else:
            return render(request,'user/cartempty.html')
        if order_qs.exists():
            order = order_qs[0]
        else:
            order= Order.objects.create(user_id=user_id.id)
        if order_qs.exists():
            orders       = order_qs[0]
            total_amount = float(orders.total_amount_cart)
            tax          = (total_amount) * 3 /100

            
                
            grand_total = float(total_amount) + float(tax)
            grand_total = "{:.1f}".format(grand_total)
            grand_total = float(grand_total)
        else:
            messages.error(request, 'Please add an product',extra_tags='ordererror')
            return render(request,'user/cartempty.html')
        context = {
            'order_object' : order_object,
            'order' : order,                
            'address' : address,
            'cart':cart_qs,
            'grand_total' :grand_total,        }
      return render(request,'user/checkout.html',context)
    
  


def selectedView(request,value):
    category = Category.objects.get(category_name = value)
    selected = category.category_name
    item     = Product.objects.filter(category = category.id).order_by("id")
    category = Category.objects.all()
    wishlist = []
    if 'user_id' in request.session:
        user      = Accounts.object.get(username = request.session['user_id'])
        wish      = MyWishList.objects.filter(username = user.id)
        for i in wish:
            wishlist.append(i.product.product_name)
        print(wishlist)
    context  = {
        'data':item,
        'category':category,
        'selected':selected,
        'wishlist':wishlist
    }
    return render(request, 'user/shop.html',context)


def deleteFromCart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect(cart)
        
