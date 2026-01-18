from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    if not order.user or not order.user.email:
        return

    subject = f"PAIRO Order Confirmed – {order.order_number}"

    message = f"""
Hi {order.user.username},

🎉 Your order has been successfully placed!

Order Number: {order.order_number}
Total Amount: ₹{order.total_amount}

🛍 Items:
"""

    for item in order.items.all():
        message += f"""
- {item.product_name}
  Size: {item.size}
  Color: {item.color}
  Qty: {item.quantity}
  Price: ₹{item.price}
"""

    message += """

Thank you for shopping with PAIRO 👟
Walk Bold. Walk PAIRO.

— Team PAIRO
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,   # IMPORTANT for debugging
    )
