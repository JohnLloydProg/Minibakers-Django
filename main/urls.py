from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.indexView.as_view(), name='home'),
    path('about/', views.aboutView.as_view(), name='about'),
    path('contact/', views.contactView.as_view(), name='contact'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),
    re_path(r'^product/(?P<product_name>.+)/$', views.ProductDetailView.as_view(), name='product_detail'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.checkout, name='checkout'),
    path('orders/', views.orders_view, name='orders'),

    #path('product/1/', views.product1, name='product1'),
    #path('product/2/', views.product2, name='product2'),
    #path('testimonials/', views.testimonials, name='testimonials')
]