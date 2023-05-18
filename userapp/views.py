from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.models import Accounts

# Create your views here.
def index(request):
    return render(request,'user/index.html')
def user_login(request):
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
                messages.error(request,'Please enter the phone Number',extra_tags='signphone_number')
                return redirect(user_signup)
            if first_name == '' or last_name =='' or username == '' or email == '' or phone_number == '' or password == '' or password1 == '':
                messages.error(request, 'Firstname must not be empty', extra_tags='signusername')
                messages.error(request, 'Lastname must not be empty', extra_tags='signusername')
                messages.error(request, 'Username must not be empty', extra_tags='signusername')
                messages.error(request, 'Email must not be empty', extra_tags='signemail')
                messages.error(request, 'Password must not be empty', extra_tags='signpass')
                messages.error(request, 'Phone number must not be empty', extra_tags='signphone_number')
                return redirect(user_signup)
            elif len(phone_number)!=10:
                messages.error(request, 'Enter corrrect phone number', extra_tags='signphone_number')
                return redirect(user_signup)
            elif Accounts.object.filter(username=username):
                messages.error(request, 'username already  exists', extra_tags='signusername')
                return redirect(user_signup)
            elif Accounts.object.filter(email=email):
                messages.error(request, 'Email already  exists', extra_tags='signemail')
                return redirect(user_signup)
            elif Accounts.object.filter(phone=phone_number):
                messages.error(request, 'Phone number already  exists', extra_tags='signphone_number')
                return redirect(user_signup)
            else:
                if Accounts.objects.filter(username=username):
                    messages.error(request, 'Username already exists', extra_tags='signusername')
                    return redirect(user_signup)
                else:
                    item = Accounts.objects.create(
                        username = username, 
                        first_name = first_name, 
                        last_name=last_name, 
                        email=email,
                        phone = phone_number,
                        password = password
                    )
                    request.session['user_id'] = username
                    item.save()
        else:
            messages.error(request, '''Password must be same 
            and must have 6 charecters''', extra_tags='signpass')
            return redirect(user_signup)
    return render(request,'user/signup.html')
def user_cart(request):
    return render(request,'user/cart.html')
def user_profile(request):
    return render(request,'user/profile.html')
def order(request):
    return render(request,'user/order.html')

