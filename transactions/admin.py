from django.contrib import admin
from .models import Receipt, Order, OrderItem

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference_number', 'payment_method', 'paid', 'paid_at')
    search_fields = ('reference_number',)
    list_filter = ('payment_method',)
    readonly_fields = ('id', 'paid_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__username', 'receipt__paid', 'total', 'pickup', 'date', 'ordered_at')
    search_fields = ('user__username', 'date')
    readonly_fields = ('id', 'ordered_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product__name', 'order__user__username', 'quantity')
    search_fields = ('product__name', 'order__user__username')
    list_filter = ('product__name',)
    readonly_fields = ('id',)

