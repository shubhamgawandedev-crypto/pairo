from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from orders.models import Order
from .utils import generate_invoice_pdf


@csrf_exempt
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return generate_invoice_pdf(order)
