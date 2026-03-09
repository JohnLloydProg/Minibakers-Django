from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def product_thumbnail_name(instance:'Product', filename:str) -> str:
    ext = filename.split('.')[-1]
    return f'product_thumbnails/{datetime.now().strftime('%Y-%b-%d_%H:%M:%S')}.{ext}'


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    thumbnail = models.ImageField(upload_to=product_thumbnail_name, blank=False, null=False)
    customizable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(default=1)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    message = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} review ({self.user.username})'
