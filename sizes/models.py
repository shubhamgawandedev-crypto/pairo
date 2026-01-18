from django.db import models


class AgeGroup(models.Model):
    label = models.CharField(max_length=30, unique=True)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.min_age}-{self.max_age})"
from categories.models import Category


class Size(models.Model):
    size_value = models.CharField(max_length=10)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sizes"
    )
    age_group = models.ForeignKey(
        AgeGroup,
        on_delete=models.CASCADE,
        related_name="sizes"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.size_value} - {self.category.name} ({self.age_group.label})"
