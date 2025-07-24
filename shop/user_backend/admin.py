from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "is_staff", "is_active", "role")
    list_filter = ("is_staff", "is_active", "role")

    fieldsets = (
        (_("Account info"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name", "phone", "avatar_url")}),
        (_("Address"), {"fields": ("city", "country", "street", "zip_code")}),
        (_("Preferences"), {"fields": ("preferred_channel",)}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email", "full_name")
    ordering = ("email",)