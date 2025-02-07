from django.db import models

from django.contrib.auth.models import User

class Enquiry(models.Model):
    name= models.CharField(max_length=15)
    email =models.EmailField(max_length=15)
    subject =models.CharField(max_length=50)
    message =models.TextField(max_length=100)



class Blog(models.Model):
    blog_name = models.CharField(max_length=50)
    blog_content =models.TextField(max_length=1000)
    blog_author = models.CharField(max_length=15)
    blog_img = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now=True)

class Sub_Blog_Image(models.Model):
    fk_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='sub_blog_images')
    name = models.CharField(max_length=50,default='default_value')
    image = models.ImageField(upload_to='sub_blog_images/')
    content = models.TextField(max_length=1000)
    
    

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men_shoes', 'Men Shoes'),
        ('women_shoes', 'Women Shoes'),
        ('kids', 'Kids'),
    ]

    product_name =models.CharField(max_length=50)
    product_image =models.ImageField(upload_to='product_image/')
    product_brand =models.CharField(max_length=50)
    product_price =models.IntegerField()
    discount_price = models.IntegerField(default=0)
    product_specifications =models.TextField(max_length=1000)
    product_highlights = models.TextField(max_length=1000)
    product_category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='men_shoes',)
    
    


class Cart(models.Model):
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    sub_total=models.DecimalField(max_digits=10, decimal_places=2)



from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Order(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.fk_user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    fk_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fk_product.product_name} (x{self.quantity})"


from django.db import models
from django.contrib.auth.models import User
from .models import Order

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('admin_contact_enquiry', 'admin_contact_enquiry'),
        ('admin_order', 'admin_order'),
        ('user_cart', 'user_cart'),
        ('user_order', 'user_order'),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for admin notifications
    count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        user_info = f" for {self.user.username}" if self.user else ""
        return f"{self.notification_type} - {self.count}{user_info}"
    
    
