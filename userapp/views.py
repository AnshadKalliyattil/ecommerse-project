from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'user/index.html')
def user_login(request):
    return render(request,'user/login.html')
def user_signup(request):  
    return render(request,'user/signup.html')
def user_cart(request):
    return render(request,'user/cart.html')
def user_profile(request):
    return render(request,'user/profile.html')

