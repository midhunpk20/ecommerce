from django.db import models

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
    product_specifications =models.TextField(max_length=1000)
    product_highlights = models.TextField(max_length=1000)
    product_category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='men_shoes',)


