from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("Email (Login)"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    zip_code = models.CharField(max_length=20, verbose_name=_("ZIP Code"))

    avatar_url = models.URLField(null=True, blank=True, verbose_name=_("Avatar / Logo / Thumbnail"))
    full_name = models.CharField(max_length=150, blank=True, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_("Phone"))

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        USER = "USER", _("User")

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER, verbose_name=_("Role"))

    class Channel(models.TextChoices):
        EMAIL = "email", _("Email")
        MAIL = "mail", _("Postal Mail")

    preferred_channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.EMAIL, verbose_name=_("Preferred Communication Channel"))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email