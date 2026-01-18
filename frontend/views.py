from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from orders.models import Order
def home(request):
    return render(request, 'home.html')

def product_detail(request, id):
    return render(request, 'product_detail.html')

def cart_page(request):
    return render(request, 'cart.html')

@login_required(login_url='/login/')
def checkout_page(request):
    return render(request, 'checkout.html')

# 🔐 AUTH VIEWS
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('/login/')
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def profile_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': orders})
