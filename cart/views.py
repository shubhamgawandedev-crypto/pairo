from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from products.models import ProductVariant
from .models import Cart
from .serializers import CartSerializer


# ============================
# 🔐 AUTHENTICATED USER CART
# ============================

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        variant = ProductVariant.objects.get(id=variant_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product_variant=variant
        )

        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return Response({"message": "Added to cart"})


class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)

        total = sum(
            item.product_variant.price * item.quantity
            for item in cart_items
        )

        return Response({
            "items": serializer.data,
            "total": total
        })


class UpdateCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, cart_id):
        quantity = int(request.data.get("quantity"))
        cart_item = Cart.objects.get(id=cart_id, user=request.user)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Cart updated"})


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_id):
        Cart.objects.filter(id=cart_id, user=request.user).delete()
        return Response({"message": "Item removed"})


# ============================
# 🟢 SESSION (GUEST) CART
# ============================

@csrf_exempt
def add_to_cart_session(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    variant_id = request.POST.get("variant_id")
    if not variant_id:
        return JsonResponse({"error": "variant_id required"}, status=400)

    cart = request.session.get("cart", {})

    if variant_id in cart:
        cart[variant_id]["quantity"] += 1
    else:
        variant = ProductVariant.objects.get(id=variant_id)
        cart[variant_id] = {
            "variant_id": variant.id,   # 🔑 IMPORTANT
            "product": variant.product.name,
            "size": variant.size.size_value,
            "color": variant.color,
            "price": float(variant.price),
            "quantity": 1,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({"message": "Added to cart"})


def cart_session_list(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for variant_id, item in cart.items():
        subtotal = item["price"] * item["quantity"]
        total += subtotal

        items.append({
            "variant_id": variant_id,
            "product": item["product"],
            "size": item["size"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

    return JsonResponse({
        "items": items,
        "total": total
    })


@csrf_exempt
def remove_from_cart_session(request, variant_id):
    cart = request.session.get("cart", {})

    variant_id = str(variant_id)
    if variant_id in cart:
        del cart[variant_id]
        request.session["cart"] = cart
        request.session.modified = True

    return JsonResponse({"message": "Item removed"})
