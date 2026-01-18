from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    product = serializers.CharField(
        source="product_variant.product.name",
        read_only=True
    )
    size = serializers.CharField(
        source="product_variant.size.size_value",
        read_only=True
    )
    color = serializers.CharField(
        source="product_variant.color",
        read_only=True
    )
    price = serializers.DecimalField(
        source="product_variant.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'product',
            'size',
            'color',
            'price',
            'quantity',
            'subtotal'
        ]

    def get_subtotal(self, obj):
        return obj.quantity * obj.product_variant.price
