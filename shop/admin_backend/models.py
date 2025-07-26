from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from user_backend.models import CustomUser


def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    ext = value.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Allowed: jpg, jpeg, png.")


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Jewelry', 'Jewelry'),
        ('Bike Accs', 'Bike Accs'),
        ('Clothing', 'Clothing'),
        ('Courses', 'Courses'),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    texture = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', validators=[validate_image_extension])


    def __str__(self):
        return f"{self.product.name} - {self.image}"

class ProductImageURL(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_urls')
    url = models.URLField()

    def __str__(self):
        return f"{self.product.name} - URL Image"

class Order(models.Model):
    class Status(models.TextChoices):
        PAID = 'paid',
        PENDING = 'pending',
        SHIPPED = 'shipped',
        DELIVERED = 'delivered',

    user = models.ForeignKey(CustomUser, related_name="orders", on_delete=models.CASCADE,)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_address = models.TextField(max_length=255)
    user_address = models.TextField(max_length=255)
    submitted_at = models.DateTimeField(default=timezone.now)
    client_full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    product_title = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=3, blank=True, null=True)
    cardholder_name = models.CharField(max_length=255, blank=True, null=True)
    buy_session_hash = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Comandă #{self.id} de la {self.client_full_name}"

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.price_per_item
        super().save(*args, **kwargs)