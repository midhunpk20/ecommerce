from django.shortcuts import render,redirect
from admin_app.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def user_register(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pword1=request.POST.get('password1')
        pword2=request.POST.get('password2')
        
        if (pword1 != pword2):
            messages.info(request,'incorrect password')
        else:
            User.objects.create_user(
                username=uname,
                password=pword2,
            ) 
            messages.success(request,'Success')
            return redirect('user_login')
    return render(request,'user_side/user_register.html')
    
def user_login(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pword=request.POST.get('password')
        user=authenticate(username=uname,password=pword)
        if user is not None:
            login(request,user)
            return redirect('user_index')
        else:
            messages.info(request,'incorrect password')
    return render(request,'user_side/user_login.html')         


def user_logout(request):
    logout(request)
    return redirect('user_login') 





def user_index(request):
    c =Product.objects.all()
    return render(request,'user_side/user_index.html',{'data':c})


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
    # Get the selected category from the query parameters
    category = request.GET.get('category', 'all')  # Default to 'all'

    # Filter products based on the category
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_category=category)

    # Render the template with the filtered products and current category
    return render(request, 'user_side/user_shop_category.html', {
        'products': products,
        'current_category': category
    })



def user_shop_product_details(request,id):
    data = Product.objects.get(id=id)

    return render(request,'user_side/user_shop_product_details.html',{'data':data})

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
    c = Blog.objects.all()
    return render(request, 'user_side/user_blog_details.html', {'data': b, 'sub_images': sub_blog_images, 'more':c })



def header_footer(request):
    user = request.user
    return render(request,'user_side/header_footer.html',{'user':user})