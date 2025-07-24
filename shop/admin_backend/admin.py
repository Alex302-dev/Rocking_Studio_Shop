from django.contrib import admin
from .models import Product, ProductImage, ProductImageURL


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


