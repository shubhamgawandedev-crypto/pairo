from django.db import models
from orders.models import Order


class Invoice(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice"
    )
    invoice_number = models.CharField(max_length=30, unique=True)
    billing_name = models.CharField(max_length=100)
    billing_phone = models.CharField(max_length=15)
    billing_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
