from django.urls import path
from . import views
from .views import contact_page, subscribe_view, product_detail_view, add_to_cart

app_name = 'guest_frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('index2/', views.index, name='index2'),
    path('products/<str:category>/', views.product_by_category, name='product_by_category'),
    path('contact/', contact_page, name='contact'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('product-detail/<int:pk>/', product_detail_view, name='product_detail_view'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/<int:cart_id>/', views.checkout_view, name='checkout'),
    path('checkout-success/', views.checkout_success_view, name='checkout_success'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]