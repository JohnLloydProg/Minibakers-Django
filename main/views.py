from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import SignUpForm

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


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'auth.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                next_page = request.GET.get('next', reverse('home'))
                return redirect(next_page)
            else:
                form.add_error(None, 'Invalid credentials')
        return render(request, 'auth.html', {'form': form})
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after successful sign up
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        remarks = request.POST.get('remarks', '')
        photo_inspo = request.FILES.getlist('photo_inspo')

        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        # Add item to session cart
        cart = request.session.get('cart', [])
        cart_item = {
            'product_id': product.id,
            'product_name': product.name,
            'quantity': quantity,
            'remarks': remarks,
            'photo_inspo': [file.name for file in photo_inspo],
            'price': product.price,
            'total_price': total_price
        }
        cart.append(cart_item)
        request.session['cart'] = cart

        return JsonResponse({'message': 'Item added to cart', 'cart': cart})

def cart_view(request):
    cart = request.session.get('cart', [])
    total_price = sum(item['total_price'] for item in cart)
    return render(request, 'cart_sidebar.html', {'cart': cart, 'total_price': total_price})