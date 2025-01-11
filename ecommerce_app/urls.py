from django.urls import path
from .views import *

urlpatterns = [
    path('register/',user_register,name='user_register'),
    path('',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),

    path('user_index',user_index,name="user_index"),
    path('Contact',user_contact,name="user_contact"),
    path('shop-category',user_shop_category,name="user_shop_category"),


    path('product_details<int:id>/',user_shop_product_details,name="user_shop_product_details"),

    
    path('product-checkout',user_shop_product_checkout,name="user_shop_product_checkout"),
    path('order-conformation',user_shop_conformation,name="user_shop_conformation"),
    path('blog',user_blog,name="user_blog"),
    path('user_blog_details/<int:id>/',user_blog_details,name="user_blog_details"),
    path('header_footer',header_footer,name="header_footer"),
    
    # Cart Add And Another Required functions
    
    path('shopcart',user_shop_shopcart,name="user_shop_shopcart"),
    path('addcart/<int:id>/',addcart,name='cartview'),
    path('plus/<int:id>/',plus,name="plus"),
    path('minus/<int:id>/',minus,name="minus"),
    path('itemdelete/<int:id>/',itemdelete,name="itemdelete"),
    
    
    
    path('book-now/<int:item_id>/',user_book_now, name='user_book_now'),
    
    path('your_order',your_order,name="your_order"),
    
    path('order-success/<int:order_id>/',order_success, name='order_success'),
    
    
]


