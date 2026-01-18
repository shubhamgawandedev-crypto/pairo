from django.urls import path
from .views import (
    AddToCartAPIView,
    CartListAPIView,
    UpdateCartAPIView,
    RemoveFromCartAPIView,
    add_to_cart_session,
    cart_session_list,
    remove_from_cart_session,
)

urlpatterns = [
    # AUTH CART
    path("", CartListAPIView.as_view()),
    path("add/", AddToCartAPIView.as_view()),
    path("update/<int:cart_id>/", UpdateCartAPIView.as_view()),
    path("remove/<int:cart_id>/", RemoveFromCartAPIView.as_view()),

    # SESSION CART
    path("add-session/", add_to_cart_session),
    path("session/", cart_session_list),
    path("remove-session/<int:variant_id>/", remove_from_cart_session),
]
