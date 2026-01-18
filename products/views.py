from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductFilterAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.filter(is_active=True)

        # Support ?subcategory=some-slug
        subcategory_slug = request.query_params.get('subcategory')
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)

        queryset = queryset.prefetch_related('images', 'variants__size')

        serializer = ProductSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, id):
        product = get_object_or_404(
            Product.objects.filter(is_active=True)
                           .prefetch_related('images', 'variants__size'),
            id=id
        )
        serializer = ProductDetailSerializer(
            product,
            context={'request': request}
        )
        return Response(serializer.data)