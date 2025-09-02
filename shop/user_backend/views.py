from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
from dataclasses import fields

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Invalid credentials')
    return render(request, 'user_backend/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')
    return render(request, 'user_backend/register.html')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        if 'save_profile' in request.POST:
            user.full_name = request.POST.get('full_name', '').strip()
            user.phone = request.POST.get('phone', '').strip()
            user.city = request.POST.get('city', '').strip()
            user.country = request.POST.get('country', '').strip()
            user.street = request.POST.get('street', '').strip()
            user.zip_code = request.POST.get('zip_code', '').strip()
            user.avatar_url = request.POST.get('avatar_url', '').strip()
            user.preffered_channel = request.POST.get('preffered_channel', user.preffered_channel)
            user.save()
            messages.success(request,'Profile updated successfully.')
            return redirect('user_backend:profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Password Changed.')
                return redirect('user_backend:profile')
            else:
                messages.error(request, 'Please correct the password form.')
    else:
        password_form = PasswordChangeForm(user)

    orders = getattr(user, 'orders', None)
    orders = orders.all().order_by('-created_at') if orders else []
    fields = ['full_name', 'phone', 'city', 'country', 'street', 'zip_code', 'avatar_url', 'preffered_channel']

    return render(request, 'user_backend/profile.html', {
        'user': user,
        'orders': orders,
        'password_form': password_form,
        'fields': fields
    })

def logout_view(request):
    logout(request)
    return redirect('/')

