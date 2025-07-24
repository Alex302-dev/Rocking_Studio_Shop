from django.db import models
from django.core.exceptions import ValidationError

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
