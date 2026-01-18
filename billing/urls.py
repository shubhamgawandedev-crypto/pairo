from django.urls import path
from .views import download_invoice

urlpatterns = [
    path("download/<int:order_id>/", download_invoice),
]
