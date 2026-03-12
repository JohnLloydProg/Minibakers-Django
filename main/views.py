from django.shortcuts import render
from django.views import View
from products.models import Product, ProductType, Product, CartItem
from transactions.models import Order, Receipt, OrderItem
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.http import JsonResponse
from datetime import datetime
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
        if isinstance(request.user, AnonymousUser):
            return redirect('login')
        
        user = request.user
        product_types = ProductType.objects.all()
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
                    'product_name': product.name,
                    'quantity': item.quantity,
                    'total_price': item_total_price,
                    'photo_inspo': item.inspo_pic,
                    'note': item.note
                })
            except Product.DoesNotExist:
                continue  # Handle the case where the product doesn't exist (optional)

        return render(request, 'cart_sidebar.html', {'cart': cart_items, 'total_price': total_price, 'categories': product_types})


def user_logout(request):
    logout(request)
    return redirect('login')


#CART FUNCTIONALITY

def add_to_cart(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')
    
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
        remarks = request.POST.get('remarks')
        pickup = request.POST.get('pickup')
        total_price = float(request.POST.get('total_price'))  # Get total price
        payment_method = request.POST.get('payment_method')

        # Get cart items
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items:
            return JsonResponse({'error': 'Your cart is empty'}, status=400)

        # Create a receipt
        receipt = Receipt.objects.create(
            paid=False,
            payment_method=payment_method,  # Handle payment method later
            reference_number=str(uuid4()),
        )

        # Create an order
        order = Order.objects.create(
            user=user,
            receipt=receipt,
            total=total_price,
            remarks=remarks,
            pickup=pickup,
            date=datetime.today().date(),
            ordered_at=datetime.now(),
        )

        total_order_price = 0

        # Copy cart items to order items
        for cart_item in cart_items:
            product = cart_item.product
            item_total_price = product.price * cart_item.quantity
            total_order_price += item_total_price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
            )

            # Delete cart item after it's added to the order
            cart_item.delete()

        # Update the total price of the order
        order.total = total_order_price
        order.save()

        return redirect(reverse('orders'))

    return JsonResponse({'error': 'Invalid method'}, status=405)


class OrderView(View):
    def get(self, request):
    # Fetch the orders for the logged-in user
        product_types = ProductType.objects.all()
        if isinstance(request.user, AnonymousUser):
            return redirect('login')
        
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', {'orders': orders, 'categories': product_types})


class CheckoutView(View):
    def get(self, request):
    # Fetch the orders for the logged-in user
        product_types = ProductType.objects.all()
        if isinstance(request.user, AnonymousUser):
            return redirect('login')
        
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum([item.product.price * item.quantity for item in cart_items])

        orders = Order.objects.filter(user=request.user)
        return render(request, 'checkout.html', {'orders': orders, 'categories': product_types, 'cart_items': cart_items, 'total_price': total_price})