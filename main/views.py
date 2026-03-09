from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType


class indexView(View):
    def get(self, request):
        return render(request, template_name='index.html')


class aboutView(View):
    def get(self, request):
        return render(request)

class contactView(View):
    def get(self, request):
        return render(request)


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
        return render(request, 'products.html', {'products':products})
    
