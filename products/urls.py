from django.urls import path
from .views import ProductFilterAPIView, ProductDetailAPIView

urlpatterns = [
    path('',               ProductFilterAPIView.as_view(), name='product-list'),
    path('<int:id>/',      ProductDetailAPIView.as_view(), name='product-detail'),
    # NO path('filter/', ...) → we removed it from frontend
]