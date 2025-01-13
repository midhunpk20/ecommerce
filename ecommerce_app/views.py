from django.shortcuts import render,redirect
from admin_app.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.core.mail import EmailMultiAlternatives  # Import this for HTML email
from django.template.loader import render_to_string  # To render HTML template
from django.utils.html import strip_tags  # To create plain text fallback

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
    c = Product.objects.all()
    for i in c:
        if i.product_price > 0 and i.discount_price > 0:
            i.discount_percentage = round(
                (i.discount_price / i.product_price) * 100
            )
            i.total_price = i.product_price - i.discount_price
        else:
            i.discount_percentage = 0
            i.total_price = i.product_price  # Default to product price if no discount

    return render(request, 'user_side/user_index.html', {'data': c})

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
        # Ensure the notification exists
        notification, created = Notification.objects.get_or_create(
            notification_type='admin_contact_enquiry',
            defaults={'count': 0}
        )
        print(f"Notification created: {created}, current count: {notification.count}")  # Debugging
        notification.count += 1
        notification.save()

                
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

    # Calculate discount percentage and total price for each product
    for i in products:
        if i.product_price > 0 and i.discount_price > 0:
            i.discount_percentage = round(
                ( i.discount_price / i.product_price) * 100
            )
            i.total_price = i.product_price - i.discount_price
        else:
            i.discount_percentage = 0
            i.total_price = i.product_price  # Default to product price if no discount

    # Render the template with the filtered products and current category
    return render(request, 'user_side/user_shop_category.html', {
        'products': products,
        'current_category': category
    })


def user_shop_product_details(request, id):
    # Retrieve the product by ID
    product = Product.objects.get(id=id)
    
    # Calculate discount percentage and total price
    if product.product_price > 0 and product.discount_price > 0:
        product.discount_percentage = round(
            (product.discount_price / product.product_price) * 100
        )
        product.total_price = product.product_price - product.discount_price
    else:
        product.discount_percentage = 0
        product.total_price = product.product_price  # Default to product price if no discount
    
    # Render the template with the product details
    return render(request, 'user_side/user_shop_product_details.html', {
        'data': product
    })


def user_shop_product_checkout(request):
    return render(request,'user_side/user_shop_product_checkout.html')

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

def addcart(request, id):
    user = User.objects.get(username=request.user.username)
    if user:
        single_product = Product.objects.get(id=id)
        
        # Assuming there's a discount field on the product model (e.g., discount_price)
        discount_price = single_product.discount_price if hasattr(single_product, 'discount_price') else 0
        
        # If a product is already in the cart, increase the quantity
        check = Cart.objects.filter(fk_product=single_product, fk_user=user).first()
        if check:
            check.quantity += 1
            # Adjust the sub_total by applying the discount
            check.sub_total = (check.quantity * (single_product.product_price - discount_price))
            check.save()
            return redirect("user_shop_shopcart")
        else:
            # If it's a new product, create a new cart item with the discount
            Cart.objects.create(
                fk_user=user,
                fk_product=single_product,
                quantity=1,
                sub_total=single_product.product_price - discount_price
            )
            
        return redirect("user_shop_shopcart")




from django.db.models import Sum



def plus(request, id):
    item = Cart.objects.get(id=id)
    item.quantity += 1
    # Assuming the product has a discount_price attribute
    discount_price = item.fk_product.discount_price if hasattr(item.fk_product, 'discount_price') else 0
    item.sub_total = (item.quantity * (item.fk_product.product_price - discount_price))
    item.save()
    return redirect("user_shop_shopcart")


def minus(request, id):
    item = Cart.objects.get(id=id)
    if item.quantity > 1:  # Ensure quantity doesn't go below 1
        item.quantity -= 1
        # Assuming the product has a discount_price attribute
        discount_price = item.fk_product.discount_price if hasattr(item.fk_product, 'discount_price') else 0
        item.sub_total = (item.quantity * (item.fk_product.product_price - discount_price))
        item.save()
    else:
        item.delete()
    return redirect("user_shop_shopcart")


def itemdelete(request,id):
    item=Cart.objects.get(id=id)
    item.delete()
    return redirect("user_shop_shopcart")


def your_order(request):
    # Get all orders of the current user
    user_orders = Order.objects.filter(fk_user=request.user).order_by('-created_at')

    # Update the notification count to 0 only for the current user
    user_order_notification = Notification.objects.filter(
        notification_type='user_order', 
        user=request.user
    ).first()

    if user_order_notification:
        # If the notification exists for the user, reset the count to 0
        user_order_notification.count = 0
        user_order_notification.save()
    else:
        # If no notification exists for the user, create one with 0 count
        Notification.objects.create(
            notification_type='user_order', 
            user=request.user, 
            count=0
        )

    # Pass orders and their items to the template
    return render(request, 'user_side/user_order.html', {
        'user_orders': user_orders,
    })


from django.shortcuts import render, redirect
from django.core.mail import send_mail
def user_shop_shopcart(request):
    # Get the cart items for the current user
    cartitem = Cart.objects.filter(fk_user=request.user).all().order_by("-id")
    
    total = 0
    count = 0
    for i in cartitem:
        count += i.quantity
        # Assuming the product has a discount_price attribute
        discount_price = i.fk_product.discount_price if hasattr(i.fk_product, 'discount_price') else 0
        total += (i.quantity * (i.fk_product.product_price - discount_price))
        
    total_cart_count = cartitem.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    
    # Update the notification count to 0 only for the current user
    user_cart_notification = Notification.objects.filter(
        notification_type='user_cart', 
        user=request.user
    ).first()
    
    if user_cart_notification:
        # If the notification exists for the user, reset the count to 0
        user_cart_notification.count = 0
        user_cart_notification.save()
    else:
        # If no notification exists for the user, create one with 0 count
        Notification.objects.create(
            notification_type='user_cart', 
            user=request.user, 
            count=0
        )

    # Render the cart page with the updated data
    return render(request, 'user_side/user_shop_shopcart.html', {
        'cartitem': cartitem,
        'total': total,
        'count': count,
        'total_cart_count': total_cart_count
    })

    
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def user_book_now(request, item_id):
    # Get the selected cart item
    cart_item = Cart.objects.filter(id=item_id, fk_user=request.user).first()

    if not cart_item:
        return render(request, 'user_side/user_buy_now.html', {
            'error': 'The selected item does not exist in your cart.'
        })

    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(
            fk_user=request.user,
            total_amount=cart_item.sub_total
        )

        # Add the selected cart item to the order
        OrderItem.objects.create(
            order=order,
            fk_product=cart_item.fk_product,
            quantity=cart_item.quantity,
            sub_total=cart_item.sub_total
        )

        # Handle shipping form submission
        name = request.POST.get('name')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')

        # Validate form fields
        if not all([name, address, city, mobile_number, email]):
            return render(request, 'user_side/user_buy_now.html', {
                'cart_item': cart_item,
                'total': cart_item.sub_total,
                'quantity': cart_item.quantity,
                'error': 'Please fill out all required fields.',
            })

        # Create shipping address
        ShippingAddress.objects.create(
            order=order,
            name=name,
            address=address,
            landmark=landmark,
            city=city,
            mobile_number=mobile_number,
            email=email
        )

        # Remove item from cart
        cart_item.delete()

        # Send confirmation email (optional, error handling is here)
        try:
            html_content = render_to_string('user_side/order_confirmation.html', {
                'user': request.user,
                'order': order,
                'name': name,
                'address': address,
                'landmark': landmark,
                'city': city,
                'mobile_number': mobile_number,
                'email': email
            })
            plain_text_content = strip_tags(html_content)
            email_message = EmailMultiAlternatives(
                subject='Order Confirmation',
                body=plain_text_content,  # Plain text content for fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],  # User-provided email address
            )
            email_message.attach_alternative(html_content, "text/html")  # Attach HTML content
            email_message.send()
        except Exception as e:
            return render(request, 'user_side/order_success.html', {
                'order': order,
                'error': f'Order placed, but email failed to send. Error: {str(e)}'
            })
            
            # Increment Admin Notification
        admin_notification, created = Notification.objects.get_or_create(
            notification_type='admin_order',
            defaults={'count': 0}
        )
        admin_notification.count += 1
        admin_notification.save()

        # Increment User Notification
        user_order_notification, created = Notification.objects.get_or_create(
        notification_type='user_order',
        user=request.user,
        defaults={'count': 0}
            )
        user_order_notification.count += 1
        user_order_notification.save()

        return redirect('order_success', order_id=order.id)

    # Handle GET request for initial load or refresh
    return render(request, 'user_side/user_buy_now.html', {
        'order': None,  # No order created yet in GET
        'cart_item': cart_item,
        'total': cart_item.sub_total,
        'quantity': cart_item.quantity,
    })

from django.shortcuts import render, get_object_or_404


def order_success(request, order_id):
    # Retrieve the order by its ID or return a 404 error if not found
    order = get_object_or_404(Order, id=order_id)
    
    # Debugging: print shipping address
    if order.shippingaddress_set.exists():
        print("Shipping Address:", order.shippingaddress_set.first())
    
    # Render the success page with the order data
    return render(request, 'user_side/order_success.html', {'order': order})





from django.http import JsonResponse

from django.http import JsonResponse

def all_addcart(request, id):
    user = User.objects.get(username=request.user.username)
    if user:
        single_product = Product.objects.get(id=id)

        # Assuming there's a discount field on the product model (e.g., discount_price)
        discount_price = single_product.discount_price if hasattr(single_product, 'discount_price') else 0

        # If a product is already in the cart, increase the quantity
        check = Cart.objects.filter(fk_product=single_product, fk_user=user).first()
        if check:
            check.quantity += 1
            # Adjust the sub_total by applying the discount
            check.sub_total = (check.quantity * (single_product.product_price - discount_price))
            check.save()
        else:
            # If it's a new product, create a new cart item with the discount
            Cart.objects.create(
                fk_user=user,
                fk_product=single_product,
                quantity=1,
                sub_total=single_product.product_price - discount_price
            )

        # Update or create admin notification (for cart items)
        user_cart_notification, created = Notification.objects.get_or_create(
            notification_type='user_cart',
            user=request.user,  # Ensure the notification is tied to the current user
            defaults={'count': 0}
        )

        # Increment the notification count for this user
        user_cart_notification.count += 1
        user_cart_notification.save()

        return JsonResponse({
            "status": "success",
            "message": "Product added to the cart." if not check else "Product quantity updated in the cart.",
            "quantity": check.quantity if check else 1,
            "sub_total": check.sub_total if check else single_product.product_price - discount_price,
        })

    return JsonResponse({"status": "error", "message": "User not found."})
