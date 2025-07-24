from django.contrib import admin
from .models import Banner, ContactPage, ContactMessage, Subscribe

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('image', 'active')
    list_filter = ('active', )

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'map_embed_code', 'phone', 'address', 'email', 'phone_icon', 'address_icon', 'email_icon')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email', )

