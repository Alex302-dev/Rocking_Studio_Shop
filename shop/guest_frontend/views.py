from urllib.request import Request

from django.shortcuts import render, redirect, get_object_or_404
from admin_backend.models import Product, ProductImage, Order, Cart, CartItem, OrderItem
from django.utils.inspect import method_has_no_args
from django.utils.crypto import get_random_string
from django.http import HttpResponse
import hashlib
from .models import Banner, ContactPage, ContactMessage, Subscribe
from collections import Counter
from django.contrib import messages
from datetime import datetime
from django.contrib import messages



def index(request):
    products = Product.objects.all()
    banner = Banner.objects.filter(active=True).first()
    categories = Product.CATEGORY_CHOICES
    current_category = request.GET.get('category')
    if current_category:
        products = products.filter(category=current_category)

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'banner': banner,
    }
    return render(request, 'guest_frontend/index.html', context)

def product_by_category(request, category):
    products = Product.objects.filter(category=category)
    categories = Product.CATEGORY_CHOICES
    return render(request, 'guest_frontend/index.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
    })

def contact_page(request):
    contact_info = ContactPage.objects.first()
    categories = Product.CATEGORY_CHOICES
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name,email=email,message=message)
            success = True
    return render(request, 'guest_frontend/contact.html', {
        'contact': contact_info,
        'success': success,
        'categories': categories,
    })

def subscribe_view(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        if email:
            if not Subscribe.objects.filter(email=email).exists():
                Subscribe.objects.create(email=email)
                messages.success(request, 'You have successfully subscribed')
            else:
                messages.info(request, 'You are already subscribed')
        else:
            messages.error(request, 'Please enter your email')
        return redirect(request.META.get('HTTP_REFERER','/'))

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'guest_frontend/product_detail.html', {
        'product': product
    })

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'guest_frontend/product_detail.html', {'product': product})

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('guest_frontend:login_required')
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'price': product.price, 'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    return redirect('guest_frontend:cart')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
    return render(request, 'guest_frontend/cart.html', {'cart': cart})

def checkout_view(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id, user=request.user, checked_out=False)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            delivery_address=request.POST.get('delivery_address', ''),
            user_address=request.POST.get('user_address', ''),
            client_full_name=request.user.full_name,
            status=Order.Status.PAID,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
        cart.checked_out = True
        cart.save()
        cart.items.all().delete()
        return redirect('guest_frontend:checkout_success')
    return render(request, 'guest_frontend/checkout.html', {'cart': cart})

def checkout_success_view(request):
    return render(request, 'guest_frontend/success.html')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__checked_out=False)
    item.delete()
    return redirect('guest_frontend:cart')

def login_required_view(request):
    return render(request, 'guest_frontend/login_required.html')

