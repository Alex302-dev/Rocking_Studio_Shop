from django.urls import path
from . import views
from .views import contact_page, subscribe_view

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<str:category>/', views.product_by_category, name='product_by_category'),
    path('contact/', contact_page, name='contact'),
    path('subscribe/', subscribe_view, name='subscribe')
]

