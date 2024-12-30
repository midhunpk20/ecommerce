from django.shortcuts import render,redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def admin_login(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('admin_home')  # Replace 'home' with your desired redirect path
        else:
            messages.error(request, "Invalid credentials.")
    return render(request,'admin_templates/admin_login.html')

def admin_home(request):
    return render(request,'admin_templates/admin_home.html')

def admin_header(request):
    user = request.user
    return render(request,'admin_templates/admin_header_footer.html',{'user':user})

from .models import Enquiry

def admin_contact(request):
    data =Enquiry.objects.all()    
    
    return render(request,'admin_templates/admin_contact.html',{'key':data})

def admin_delete(request,id):
    dele =Enquiry.objects.get(id=id)
    dele.delete()

    return redirect("admin_enquiry")

from .models import Blog

def admin_blog(request):
    if request.method =='POST':
        a =request.POST.get("s_blog_name")
        b =request.POST.get("s_blog_content")
        c =request.POST.get("s_blog_author")
        d =request.FILES.get("s_blog_img",None)

        

        Blog.objects.create(

            blog_name =a,
            blog_content =b,
            blog_author =c,
            blog_img =d,
             
            
        )
        
        return redirect("blog_list")
    return render(request,'admin_templates/admin_blog.html')


def blog_list(request):

    blog = Blog.objects.all()
    return render(request,'admin_templates/blog_list.html',{'blog':blog})

def blog_delete(request,id):
    dele =Blog.objects.get(id=id)
    dele.delete()

    return redirect('blog_list')

def blog_edit(request,id):
    data= Blog.objects.get(id=id)

    if request.method=="POST":
        a =request.POST.get("s_blog_name")
        b =request.POST.get("s_blog_content")
        c =request.POST.get("s_blog_author")
        d =request.FILES.get("s_blog_img",None)


        if a:
            data.blog_name =a
        if b:
            data.blog_content =b   
        if c:
            data.blog_author =c
        if d:
            data.blog_img =d        

        data.save()     

        return redirect("blog_list")                              


    return render(request,'admin_templates/blog_edit.html',{'data':data}) 
       

def blog_view(request,id):
    data = Blog.objects.get(id=id)
    
    return render(request,'admin_templates/blog_view.html',{'data':data})



# Sub Blog Images Code CRUD

from .models import Sub_Blog_Image

def create_sub_blog_image(request):
    blog = Blog.objects.all()

    if request.method == 'POST':
        image = request.FILES['s_sub_image']
        blog_id = request.POST.get('blog_name')
        selected_blog = Blog.objects.get(id=blog_id) 
        content =request.POST.get('blog_content')
        
        # Create a new Sub_Blog_Image
        Sub_Blog_Image.objects.create(
            fk_blog=selected_blog,  # Associate the image with the selected blog
            image=image,
            content=content

        )
        return redirect("sub_img_list")

    return render(request, 'admin_templates/sub_blog_create.html', {'blog': blog})


def list_sub_img_list(request):
    a = Sub_Blog_Image.objects.all()
    return render(request,'admin_templates/sub_img_list.html',{'a':a})

def delete_sub_img(request,id):
    dele =Sub_Blog_Image.objects.get(id=id)
    dele.delete()

    return redirect('sub_img_list')

def edit_sub_img(request, id):
    data = Sub_Blog_Image.objects.get(id=id)
    blogs = Blog.objects.all()  # Fetch all Blog objects for dropdown options

    if request.method == "POST":
        blog_id = request.POST.get('blog_name')  
        content = request.POST.get('blog_content') 
        image = request.FILES.get('s_sub_img', None)  
 
        # Update fields if new values are provided
        if blog_id:
            selected_blog = Blog.objects.get(id=blog_id)
            data.fk_blog = selected_blog 
        if content:
            data.content = content
        if image:
            data.image = image

       
        data.save()

        return redirect("sub_img_list")

    return render(request, 'admin_templates/sub_img_edit.html', {'data': data, 'blogs': blogs})

       

def view_sub_img(request,id):
    data = Sub_Blog_Image.objects.get(id=id)
    
    return render(request,'admin_templates/sub_img_view.html',{'data':data})


#product CRUD

from .models import Product

from django.shortcuts import render, redirect
from .models import Product

def product_add(request):
    if request.method == "POST":
        a = request.POST.get("product_name")
        b = request.FILES.get("product_image")  # Use FILES for image upload
        c = request.POST.get("product_brand")
        d = request.POST.get("product_price")
        e = request.POST.get("product_specifications")
        f = request.POST.get("product_highlights")
        g = request.POST.get("product_category")

        # Validate and handle missing/invalid data if necessary
        Product.objects.create(
            product_name=a,
            product_image=b,
            product_brand=c,
            product_price=d,
            product_specifications=e,
            product_highlights=f,
            product_category=g,
        )
        return redirect('list_product')  # Replace 'product_list' with the actual name of your URL pattern
    return render(request, 'admin_templates/product_add.html')  # Replace 'your_template_name.html' with your form template name


def list_product(request):

    products = Product.objects.all()
    
    return render(request,'admin_templates/list_product.html',{'products':products})


def delete_product(request,id):
    dele =Product.objects.get(id=id)
    dele.delete()

    return redirect('list_product')

def edit_product(request,id):
    data= Product.objects.get(id=id)

    if request.method=="POST":
        a = request.POST.get("product_name")
        b = request.FILES.get("product_image")  # Use FILES for image upload
        c = request.POST.get("product_brand")
        d = request.POST.get("product_price")
        e = request.POST.get("product_specifications")
        f = request.POST.get("product_highlights")
        g = request.POST.get("product_category")


        if a:
            data.product_name =a
        if b:
            data.product_image =b   
        if c:
            data.product_brand =c
        if d:
            data.product_price =d 
        if e:
            data.product_specifications =e
        if f:
            data.product_highlights =f 
        if g:
            data.product_category =g

        data.save()     

        return redirect("list_product")                              


    return render(request,'admin_templates/edit_product.html',{'data':data}) 
       

def view_product(request,id):
    data = Product.objects.get(id=id)
    
    return render(request,'admin_templates/view_product.html',{'data':data}) 

def add_cart(request,product_id):
    return render(request,'admin_templates/add_to_cart.html')



