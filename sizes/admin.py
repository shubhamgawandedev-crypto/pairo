from django.contrib import admin
from .models import AgeGroup, Size


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('label', 'min_age', 'max_age', 'is_active')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size_value', 'category', 'age_group', 'is_active')
    list_filter = ('category', 'age_group')
