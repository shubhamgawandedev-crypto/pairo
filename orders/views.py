import uuid
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from products.models import ProductVariant
from cart.models import Cart
from .models import Order, OrderItem
from .email_utils import send_order_confirmation_email


# 🔐 AUTH / JWT CHECKOUT (FOR FUTURE)
class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        subtotal = sum(
            item.product_variant.price * item.quantity
            for item in cart_items
        )

        tax = subtotal * Decimal("0.18")
        total = subtotal + tax

        order = Order.objects.create(
            user=request.user,
            order_number=f"PAIRO-{uuid.uuid4().hex[:8].upper()}",
            subtotal=subtotal,
            tax_amount=tax,
            total_amount=total,
            status="PLACED",
        )

        for item in cart_items:
            variant = item.product_variant

            if variant.stock < item.quantity:
                return Response({"error": "Insufficient stock"}, status=400)

            OrderItem.objects.create(
                order=order,
                product_name=variant.product.name,
                size=variant.size.size_value,
                color=variant.color,
                price=variant.price,
                quantity=item.quantity,
            )

            variant.stock -= item.quantity
            variant.save()

        cart_items.delete()

        # 📧 SEND EMAIL
        send_order_confirmation_email(order)

        return Response({
            "message": "Order placed successfully",
            "order_number": order.order_number,
            "total": float(total),
        })


# 🟢 SESSION BASED CHECKOUT (HTML + JS)
@csrf_exempt
def checkout_session(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Login required to place order"},
            status=401
        )

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    cart = request.session.get("cart", {})

    if not cart:
        return JsonResponse({"error": "Cart is empty"}, status=400)

    subtotal = Decimal("0.00")

    for item in cart.values():
        subtotal += Decimal(str(item["price"])) * item["quantity"]

    tax = subtotal * Decimal("0.18")
    total = subtotal + tax

    order = Order.objects.create(
        user=request.user,
        order_number=f"PAIRO-{uuid.uuid4().hex[:8].upper()}",
        subtotal=subtotal,
        tax_amount=tax,
        total_amount=total,
        status="PLACED",
    )

    for variant_id, item in cart.items():
        variant = ProductVariant.objects.get(id=variant_id)

        if variant.stock < item["quantity"]:
            return JsonResponse({"error": "Insufficient stock"}, status=400)

        OrderItem.objects.create(
            order=order,
            product_name=item["product"],
            size=item["size"],
            color=item["color"],
            price=item["price"],
            quantity=item["quantity"],
        )

        variant.stock -= item["quantity"]
        variant.save()

    # 📧 SEND EMAIL (USER IS LOGGED IN)
    send_order_confirmation_email(order)

    # clear session cart
    request.session["cart"] = {}
    request.session.modified = True

    return JsonResponse({
        "message": "Order placed successfully",
        "order_id": order.id,
        "order_number": order.order_number,
        "total": float(total),
    })
