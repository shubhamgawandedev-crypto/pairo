from django.urls import path
from .views import (
    home,
    product_detail,
    cart_page,
    checkout_page,
    login_view,
    signup_view,
    logout_view, profile_page
)

urlpatterns = [
    # Pages
    path('', home, name='home'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),

    # Auth
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_page, name='profile'),
]
