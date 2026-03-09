from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType


class indexView(View):
    def get(self, request):
        return render(request, 'index.html')


class aboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class contactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        context = {
            'success': 'Your suggestion has been sent successfully!',
            'name': name,
            'email': email,
            'message': message
        }

        return render(request, 'contact.html', context)


class ProductView(View):
    def get(self, request):
        
        product_types = ProductType.objects.all()

        products = []
        for _type in product_types:
            products.append({
                'category': _type.name,
                'items': Product.objects.filter(type__id=_type.pk)
            }) 
        print(products)
        return render(request, 'products.html', {'products':products, 'categories':product_types})
    

class TestimonialsView(View):
    def get(self, request):
        return render(request, 'testimonials.html')