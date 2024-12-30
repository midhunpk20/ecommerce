from django.urls import path
from .views import *

urlpatterns = [
    path('',user_index,name="user_index"),
    path('Contact',user_contact,name="user_contact"),
    path('shop-category',user_shop_category,name="user_shop_category"),


    path('product_details<int:id>/',user_shop_product_details,name="user_shop_product_details"),

    
    path('product-checkout',user_shop_product_checkout,name="user_shop_product_checkout"),
    path('shopcart',user_shop_shopcart,name="user_shop_shopcart"),
    path('order-conformation',user_shop_conformation,name="user_shop_conformation"),
    path('blog',user_blog,name="user_blog"),
    path('user_blog_details/<int:id>/',user_blog_details,name="user_blog_details"),
    path('header_footer',header_footer,name="header_footer")
    
]