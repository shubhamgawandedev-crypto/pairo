from rest_framework import serializers
from django.conf import settings
from .models import Product, ProductVariant, ProductImage
from categories.models import SubCategory


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["image", "is_primary"]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            # fallback when request context is missing (e.g. some tests / background tasks)
            return obj.image.url
        return None


class ProductVariantSerializer(serializers.ModelSerializer):
    # Safe handling if size is missing or null
    size = serializers.CharField(
        source="size.size_value",
        read_only=True,
        allow_null=True,
        default="N/A"
    )

    class Meta:
        model = ProductVariant
        fields = ["id", "size", "color", "price", "stock"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "brand", "base_price", "images"]


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    # FIXED: removed redundant source="variants"
    # When field name == related_name, source is not needed
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "description",
            "base_price",
            "images",
            "variants",
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']