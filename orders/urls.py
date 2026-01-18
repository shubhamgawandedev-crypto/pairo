from django.urls import path
from .views import CheckoutAPIView, checkout_session

urlpatterns = [
    # JWT / AUTH (future use)
    path("checkout/", CheckoutAPIView.as_view()),

    # Session-based checkout (HTML + JS)
    path("checkout-session/", checkout_session),
]
