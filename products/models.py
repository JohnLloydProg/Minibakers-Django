from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def order_inspo_pic_name(instance:'CartItem', filename:str)-> str:
    ext = filename.split('.')[-1]
    return f'order_inspo_pics/{datetime.now().strftime('%Y-%b-%d_%H:%M:%S')}.{ext}'

def product_thumbnail_name(instance:'Product', filename:str) -> str: #MAIN IMAGE
    ext = filename.split('.')[-1]
    return f'product_thumbnails/{datetime.now().strftime('%Y-%b-%d_%H:%M:%S')}.{ext}'

def product_type_thumbnail_name(instance:'Product', filename:str) -> str:
    ext = filename.split('.')[-1]
    return f'product_type_thumbnails/{datetime.now().strftime('%Y-%b-%d_%H:%M:%S')}.{ext}'

def product_image_name(instance: 'ProductImage', filename: str) -> str:
    ext = filename.split('.')[-1]  # Get file extension
    product_name = instance.product.name  # Use product name as folder name
    return f'products/{product_name}/images/{datetime.now().strftime("%Y-%b-%d_%H-%M-%S")}.{ext}'

class ProductType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    thumbnail = models.ImageField(upload_to=product_type_thumbnail_name, blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    thumbnail = models.ImageField(upload_to=product_thumbnail_name, blank=False, null=False)
    customizable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to=product_image_name, blank=False, null=False)  # Custom path for product images
    
    def __str__(self):
        return f"Image for {self.product.name}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(default=1)
    inspo_pic = models.ImageField(upload_to=order_inspo_pic_name, blank=True, null=True)
    note = models.TextField()

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f" (Product: {self.product.name}, User: {self.user.username}, Quantity: {self.quantity})"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    message = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} review ({self.user.username})'
