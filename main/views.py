from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType, Product, CartItem
from transactions.models import Order, Receipt, OrderItem
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from uuid import uuid4
from django.http import JsonResponse
from datetime import datetime
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



class CartView(View):
    def get(self, request):
        # Retrieve the current user
        user = request.user

        # Fetch the user's cart items from the products_cartitem table
        cart_items_db = CartItem.objects.filter(user_id=user.id)

        cart_items = []
        total_price = 0

        for item in cart_items_db:
            try:
                product = Product.objects.get(id=item.product_id)  # Fetch the product by ID
                item_total_price = product.price * item.quantity  # Calculate total price per item
                total_price += item_total_price  # Add to the overall total price

                cart_items.append({
                    'product': product,
                    'quantity': item.quantity,
                    'total_price': item_total_price,
                })
            except Product.DoesNotExist:
                continue  # Handle the case where the product doesn't exist (optional)

        return render(request, 'cart_sidebar.html', {'cart': cart_items, 'total_price': total_price})


def user_logout(request):
    logout(request)
    return redirect('login')


#CART FUNCTIONALITY

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        remarks = request.POST.get('remarks')
        photo_inspo = request.FILES.get('photo_inspo')  # File from the request

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        user = request.user  # Using logged-in user's ID directly

        # Check if the product is already in the cart (products_cartitem)
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity},
            note=remarks,
            inspo_pic=photo_inspo
        )

        if not created:
            # If the item already exists in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'message': 'Item added to cart'}, status=200)

    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required
def create_order(request):
    if request.method == 'POST':
        user = request.user
        total_price = float(request.POST.get('total_price'))  # Get total price from the frontend

        # Get the cart items for the user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items:
            return JsonResponse({'error': 'Your cart is empty'}, status=400)

        # Create a receipt
        receipt = Receipt.objects.create(
            paid=False,
            payment_method='Pending',  # This can be updated later based on the payment method
            reference_number=str(uuid4()),  # Generate a unique reference number
        )

        # Create the order
        order = Order.objects.create(
            user=user,
            receipt=receipt,
            total=total_price,
            date=datetime.today().date(),
            ordered_at=datetime.now(),
        )

        # Loop through the cart items and create order items
        for cart_item in cart_items:
            product = cart_item.product
            item_total_price = product.price * cart_item.quantity

            # Create the order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                inspo_pic=cart_item.photo_inspo,  # Copy the inspo photo if exists
                note=cart_item.remarks,  # Copy remarks from cart item
            )

            # Optional: Delete the cart item after adding to the order
            cart_item.delete()

        return JsonResponse({'success': True, 'order_id': order.id}, status=200)

    return JsonResponse({'error': 'Invalid method'}, status=405)