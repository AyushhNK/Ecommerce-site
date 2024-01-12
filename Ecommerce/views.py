from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,authenticate,logout
from .forms import SignUpForm
from .models import Product,Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
	user=request.user
	obj=Product.objects.all()
	return render(request,"home.html",{"name":user,"objects":obj})

def log_in(request):
	if request.method=="POST":
		form=AuthenticationForm(request,data=request.POST)
		if form.is_valid():
			username=form.cleaned_data["username"]
			password=form.cleaned_data["password"]
			user=authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect("home")
	else:
		form=AuthenticationForm()
	return render(request,"login.html",{"form":form})


def signup(request):
	if request.method=="POST":
		form=SignUpForm(request.POST)
		if form.is_valid():
			user=form.save()
			login(request,user)
			return redirect("home")
	else:
		form=SignUpForm()
	return render(request,"signup.html",{"form":form})

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
	user=request.user
	user_cart= Cart.objects.get(user=request.user)
	cart_items= CartItem.objects.filter(cart=user_cart)
	total=0
	for i in cart_items:
		total=i.quantity*i.product.price
	return render(request,"cart.html",{"items":cart_items,"totaldue":total,"name":user})



@login_required
def remove_from_cart(request, cart_item_id):
	cart_item = CartItem.objects.filter(id=cart_item_id)
	for item in cart_item:
		if item.quantity>1:
			item.quantity-=1
			item.save()
		else:
			item.delete()
	return redirect("items_cart")
	