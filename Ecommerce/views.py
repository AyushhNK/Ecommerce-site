from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
from django.db.models import Q

# def home(request):
#     user = request.user
#     obj = Product.objects.all()
#     return render(request, "home.html", {"name": user, "objects": obj})

def home(request):
    user = request.user
    query = request.GET.get('q')
    
    if query:
        if query=="all":
            obj = Product.objects.all()
        obj = Product.objects.filter(
            Q(name__icontains=query)
        )
    else:
        obj = Product.objects.all()    
    return render(request, "home.html", {"name": user, "objects": obj, "query": query})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('home')
        else:
            # Return an error message or render the login page with an error
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'signup.html', {'error': 'Invalid'})
    return render(request, "signup.html", {"form": form})

def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

@login_required
def items_in_cart(request):
    user = request.user
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total = 0
    for i in cart_items:
        total += i.quantity * i.product.price
    return render(request, "cart.html", {"items": cart_items, "totaldue": total, "name": user})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.filter(id=cart_item_id)
    for item in cart_item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return redirect("items_cart")

def CheckoutView(request, totaldue):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    data={
        "return_url": "http://localhost:8000/",
        "website_url": "http://localhost:8000/",
        "amount": f"{totaldue*1000}", 
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        "customer_info": {
            "name": "ayush",
            "email": "test@khalti.com",
            "phone": "9800000001"
        }
    }

    payload = json.dumps(data)
    headers = {
        'Authorization': 'Key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()
        payment_url = response_data.get('payment_url')
        return redirect(payment_url)

def index(request):
    return render(request, "index.html")
