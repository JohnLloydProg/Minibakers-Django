from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from datetime import datetime
from uuid import uuid4

def order_inspo_pic_name(instance:'OrderItem', filename:str)-> str:
    ext = filename.split('.')[-1]
    return f'order_inspo_pics/{datetime.now().strftime('%Y-%b-%d_%H:%M:%S')}.{ext}'


class Receipt(models.Model):
    paid = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=False, null=False)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payment_method} ({self.reference_number})' if self.reference_number else f'{self.payment_method} ({self.pk})'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=False, null=False)
    products = models.ManyToManyField(Product, through='OrderItem')
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE)
    remarks = models.TextField()
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    pickup = models.BooleanField(default=True)
    date = models.DateField(blank=False, null=False)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    inspo_pic = models.ImageField(upload_to=order_inspo_pic_name, blank=True, null=True)
    note = models.TextField()
