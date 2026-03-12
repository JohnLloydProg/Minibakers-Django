from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType


class indexView(View):
    def get(self, request):
        product_types = ProductType.objects.all()
        products = Product.objects.all()
        print(product_types)
        return render(request, 'index.html', {'categories': product_types, 'products': products})


class aboutView(View):
    def get(self, request):
        product_types = ProductType.objects.all()

        return render(request, 'about.html', {'categories': product_types})

class contactView(View):
    def get(self, request):
        product_types = ProductType.objects.all()

        return render(request, 'contact.html', {'categories': product_types})

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
    
class ProductDetailView(View):
    def get(self, request, product_name):
        # Slugify the product name if needed for URL-friendly handling
        product = Product.objects.filter(name__iexact=product_name).first()
        product_types = ProductType.objects.all()
        if not product:
            return render(request, '404.html')  # or return a custom error page
        
        # Assuming the template needs 'product' as context
        return render(request, 'product_detail.html', {'product': product, 'categories':product_types})


class TestimonialsView(View):
    def get(self, request):
        product_types = ProductType.objects.all()
        return render(request, 'testimonials.html', {'categories': product_types})