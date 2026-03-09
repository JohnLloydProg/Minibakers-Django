from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView.as_view(), name='home'),
    path('about/', views.aboutView.as_view(), name='about'),
    path('contact/', views.contactView.as_view(), name='contact'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials')
    #path('product/1/', views.product1, name='product1'),
    #path('product/2/', views.product2, name='product2'),
    #path('testimonials/', views.testimonials, name='testimonials')
]