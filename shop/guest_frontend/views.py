from urllib.request import Request

from django.shortcuts import render, redirect
from admin_backend.models import Product, ProductImage
from .models import ContactPage, Banner, ContactMessage, Subscribe
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



