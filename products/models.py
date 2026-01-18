from django.db import models
from categories.models import SubCategory
from sizes.models import Size


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, default="PAIRO")
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"   # ← correct related_name
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    color = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size.size_value} - {self.color}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"     # ← correct related_name
    )
    image = models.ImageField(upload_to="")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image of {self.product.name}"   # FIXED: removed trailing comma

    class Meta:
        ordering = ['id']