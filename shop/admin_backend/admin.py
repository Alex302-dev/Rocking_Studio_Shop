from django.contrib import admin
from .models import Product, ProductImage, ProductImageURL, Order, OrderItem
from django.utils.translation import gettext_lazy as _

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductImageURLInline(admin.TabularInline):
    model = ProductImageURL
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'texture', 'price')
    list_filter = ('category', )
    search_fields = ('name', )
    inlines = [ProductImageInline, ProductImageURLInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

@admin.register(ProductImageURL)
class ProductImageURLAdmin(admin.ModelAdmin):
    list_display = ('product', 'url')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client_full_name',
        'total_cost',
        'status',
        'submitted_at',
    )
    list_filter = ('status', 'submitted_at')
    search_fields = ('client_full_name', 'user__email')
    readonly_fields = ('submitted_at', 'total_cost', 'buy_session_hash')
    fieldsets = (
        (_('Order Details'), {
            'fields': (
                'user',
                'client_full_name',
                'total_cost',
                'status',
            )
        }),
        (_('Addresses'), {
            'fields': ('user_address', 'delivery_address'),
        }),
        (_('Card Info'), {
            'fields': (
                'cardholder_name',
                'card_number',
                'card_expiry',
                'card_cvv',
                'buy_session_hash',
            )
        }),
        (_('Meta'), {
            'fields': ('submitted_at',),
        }),
    )
