from django.urls import path
from . import views
from .views import profile_view

app_name = 'user_backend'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', profile_view, name='profile')
]