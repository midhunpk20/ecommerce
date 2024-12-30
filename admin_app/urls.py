from django.urls import path
from .views import *

urlpatterns = [
    path('',admin_login,name="admin_login"),
    path('admin_home',admin_home,name="admin_home"),
    path('admin_header',admin_header,name="admin_header"),
    path('admin_contact',admin_contact,name="admin_enquiry"),
    path('admin_user_delete/<int:id>',admin_delete,name ="delete_enquiry"),
    path('admin_blog',admin_blog,name = "admin_blog"),
    path('blog_table',blog_list,name="blog_list"),
    path('blog_delete/<int:id>',blog_delete,name = "delete_blog"),
    path('blog_edit/<int:id>',blog_edit,name= "edit_blog"),
    path('blog_view/<int:id>',blog_view,name="view_blog"),  

    # Sub Blog Image Add Code
    path('sub_img_list',list_sub_img_list,name="sub_img_list"), 
    path('sub_blog_create',create_sub_blog_image,name="sub_blog_create"),
    path('sub_img_delete/<int:id>',delete_sub_img,name="sub_img_delete"),
    path('sub_img_edit/<int:id>',edit_sub_img,name="sub_img_edit"),
    path('sub_img_view/<int:id>',view_sub_img,name="sub_img_view"),

    #product 

    path('product_add',product_add,name="product_add"),
    path('list_products',list_product,name="list_product"),
    path('product_delete/<int:id>',delete_product,name="product_delete"),
    path('product_edit/<int:id>',edit_product,name="product_edit"),
    path('product_view/<int:id>',view_product,name="product_view")
    
    ]

    # add to cart
    