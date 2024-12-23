from django.shortcuts import render,redirect
from admin_app.models import *

def user_index(request):
    return render(request,'user_side/user_index.html')


# from admin_app.models import Enquiry

def user_contact(request):
    if request.method =="POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        Enquiry.objects.create(
            name = username,
            email = email,
            subject = subject,
            message = message
        )
        return redirect("user_index")
    return render(request,'user_side/user_contact.html')

def user_shop_category(request):
    return render(request,'user_side/user_shop_category.html')

def user_shop_product_details(request):
    return render(request,'user_side/user_shop_product_details.html')

def user_shop_product_checkout(request):
    return render(request,'user_side/user_shop_product_checkout.html')

def user_shop_shopcart(request):
    return render(request,'user_side/user_shop_shopcart.html')

def user_shop_conformation(request):
    return render(request,'user_side/user_shop_conformation.html')

def user_blog(request):
    a = Blog.objects.all()
    return render(request,'user_side/user_blog.html',{'data':a})

def user_blog_details(request, id):
    b = Blog.objects.get(id=id)
    sub_blog_images = Sub_Blog_Image.objects.filter(fk_blog=b)  # Correct syntax for filtering
    return render(request, 'user_side/user_blog_details.html', {'data': b, 'sub_images': sub_blog_images})

def header_footer(request):
    return render(request,'user_side/header_footer.html')