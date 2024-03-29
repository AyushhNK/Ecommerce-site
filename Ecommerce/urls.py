from django.urls import path
from . import views

urlpatterns=[
    path("index",views.index,name="index"),
	path("",views.home,name="home"),
	path("signin/",views.signin,name="signin"),
	path("signup/",views.signup,name="signup"),
	path("logout/",views.log_out,name="log_out"),
	path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
	path('usercart/',views.items_in_cart,name="items_cart"),
	path('removecart/<int:cart_item_id>',views.remove_from_cart,name="remove_cart"),
	path('checkout/<int:totaldue>',views.CheckoutView,name="checkout"),
]