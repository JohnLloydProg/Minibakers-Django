from django.contrib import admin
from .models import Product, CartItem, Review, ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'customizable', 'created_at')
    search_fields = ('name',)
    list_filter = ('customizable',)
    readonly_fields = ('id', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product__name', 'user__username', 'quantity')
    search_fields = ('product__name', 'user__username')
    list_filter = ('product__name',)
    readonly_fields = ('id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product__name', 'user__username', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('product__name', 'rating')
    readonly_fields = ('id', 'created_at')


