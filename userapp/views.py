from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.models import Accounts
from django.contrib.auth import authenticate

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
                        username = username, 
                        email=email,
                        phone = phone_number,
                        password = password
                    )
                    item.set_password(password)
                    item.save()
                    request.session['user_id'] = username
                
        else:
            messages.error(request, '''Password must be same 
            and must have 6 charecters''')
            return redirect(user_signup)
    return render(request,'user/signup.html')
def user_cart(request):
    return render(request,'user/cart.html')
def user_profile(request):
    return render(request,'user/profile.html')
def order(request):
    return render(request,'user/order.html')
def forgot_password(request):
    return render(request,'user/forgot_password.html')
def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect(index)
    return render(request,'user/login.html')



