from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_invoice_pdf(order):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{order.order_number}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "PAIRO SHOES")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Order No: {order.order_number}")
    c.drawString(50, height - 100, f"Status: {order.status}")

    # Items
    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Items")

    y -= 20
    c.setFont("Helvetica", 10)

    for item in order.items.all():
        line = (
            f"{item.product_name} | Size {item.size} | "
            f"{item.color} | Qty {item.quantity} | ₹{item.price}"
        )
        c.drawString(50, y, line)
        y -= 15

    # Totals
    y -= 20
    c.drawString(50, y, f"Subtotal: ₹{order.subtotal}")
    y -= 15
    c.drawString(50, y, f"GST (18%): ₹{order.tax_amount}")
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: ₹{order.total_amount}")

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 60, "Thank you for shopping with PAIRO 👟")

    c.showPage()
    c.save()

    return response
