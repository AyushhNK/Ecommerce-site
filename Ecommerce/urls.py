from django.urls import path
from . import views

urlpatterns=[
	path("",views.home,name="home"),
	path("login/",views.log_in,name="log_in"),
	path("signup/",views.signup,name="signup"),
	path("logout/",views.log_out,name="log_out"),
	path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
	path('usercart/',views.items_in_cart,name="items_cart"),
	path('removecart/<int:cart_item_id>',views.remove_from_cart,name="remove_cart"),
]