from urllib.request import Request

from django.shortcuts import render, redirect, get_object_or_404
from admin_backend.models import Product, ProductImage, Order
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
        'success':success
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
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(pk)] = cart.get(str(pk), 0) + 1  # Increment quantity
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('guest_frontend:cart', product_id=pk)

def cart_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Create or retrieve an order object for the current session/user
    order = Order.objects.filter(user=request.user, status=Order.Status.PENDING).first()

    if not order:
        order = Order.objects.create(
            user=request.user,
            delivery_address="",
            user_address="",
            client_full_name = request.user.full_name,
            product_title=product.name,
            quantity=1,
            price_per_item=product.price
        )

    return render(request, 'guest_frontend/cart.html', {
        'product': product,
        'order': order,
    })

def checkout_view(request, order_id):
  order = get_object_or_404(Order, pk=order_id)
  if request.method == 'POST':
    card_number = request.POST.get('card_number', '').strip()
    card_expiry = request.POST.get('card_expiry', '').strip()
    card_cvv = request.POST.get('card_cvv', '').strip()
    cardholder_name = request.POST.get('cardholder_name', '').strip()
    errors = []
    if not card_number.isdigit() or len(card_number) != 16:
      errors.append("Card number must be exactly 16 digits.")
    if not card_cvv.isdigit() or len(card_cvv) != 3:
      errors.append("CVV must be exactly 3 digits.")
    if not cardholder_name or len(cardholder_name.split()) < 2:
      errors.append("Cardholder name must contain at least two words.")
    if not card_expiry or len(card_expiry) != 5 or card_expiry[2] != '/':
      errors.append("Expiration date must be in MM/YY format.")
    else:
      try:
        month, year = map(int, card_expiry.split('/'))
        if not (1 <= month <= 12):
          raise ValueError
        expiry_date = datetime.strptime(f"{month}/20{year}", "%m/%Y")
        if expiry_date < datetime.now().replace(day=1):
          errors.append("Expiration date must be in the future.")
      except ValueError:
        errors.append("Invalid expiration date format.")
    if errors:
      for error in errors:
        messages.error(request, error)
      return render(request, 'guest_frontend/checkout.html', {
        'order': order,
        'total': order.total_cost
      })
    session_data = f"{card_number}{card_expiry}{cardholder_name}{get_random_string(8)}"
    buy_session_hash = hashlib.sha256(session_data.encode()).hexdigest()
    order.card_number = card_number
    order.card_expiry = card_expiry
    order.card_cvv = card_cvv
    order.cardholder_name = cardholder_name
    order.buy_session_hash = buy_session_hash
    order.status = Order.Status.PAID
    order.save()
    if 'cart' in request.session:
      del request.session['cart']
      request.session.modified = True
    return redirect('guest_frontend:checkout_success')
  return render(request, 'guest_frontend/checkout.html', {
    'order': order,
    'total': order.total_cost
  })

def checkout_success_view(request):
    return render(request, 'guest_frontend/success.html')

