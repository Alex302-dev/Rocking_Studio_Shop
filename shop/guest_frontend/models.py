from django.db import models
from django.db.models import Model, ImageField, BooleanField, CharField, TextField, EmailField, DateTimeField
from django.utils.translation import gettext_lazy as _

class Banner(Model):
    image = ImageField(upload_to='banners/', null=True, blank=True)
    active = BooleanField(default=True, null=True, blank=True)
    title = CharField(max_length=255, null=True, blank=True)
    subtitle = CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return f"Banner {self.pk}"

class ContactPage(Model):
    title = CharField(max_length=255, null=True, blank=True)
    subtitle = CharField(max_length=255, null=True, blank=True)
    map_embed_code = TextField(null=True, blank=True)
    phone = CharField(max_length=255, null=True, blank=True)
    address = TextField(null=True, blank=True)
    email = EmailField(null=True, blank=True)
    phone_icon = CharField(max_length=255, null=True, blank=True)
    address_icon = CharField(max_length=255, null=True, blank=True)
    email_icon = CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Contact Page')
        verbose_name_plural = _('Contact Pages')

    def __str__(self):
        return self.title or "Contact Page"


class ContactMessage(Model):
    name = CharField(max_length=255, null=True, blank=True)
    email = EmailField(max_length=255, null=True, blank=True)
    message = TextField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= _('Contact Message')
        verbose_name_plural = _('Contact Messages')

    def __str__(self):
        return f'{self.name} - {self.email}'

class Subscribe(Model):
    email = EmailField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')

    def __str__(self):
        return self.email