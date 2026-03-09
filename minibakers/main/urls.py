from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView.as_view(), name='index'),
    path('about/', views.aboutView.as_view(), name='about'),
    path('contact/', views.contactView, name='contact'),
    path('product/1/', views.product1, name='product1'),
    path('product/2/', views.product2, name='product2'),
    path('testimonials/', views.testimonials, name='testimonials')
]