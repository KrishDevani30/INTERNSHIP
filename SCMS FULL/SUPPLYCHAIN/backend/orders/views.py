from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
import os

from .models import Customer, Order, Item, StatusHistory
from .serializers import OrderSerializer

import sendgrid
from sendgrid.helpers.mail import Mail

# 🔐 Configure SendGrid API key and sender email here
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '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')  # Get from environment variable
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'kingisright67@gmail.com')  # Get from environment variable

# 🔧 Stage-wise responsible person email mapping
STAGE_EMAILS = {
    'Material': 'krrishmiraj12345@gmail.com',
    'Manufacturing': 'yashbharvada4@gmail.com',
    'Packaging': 'yashbharvada4@gmail.com',
    'Dispatch': 'princediyora05@gmail.com',
    'Completed': 'kingisright67@gmail.com',
}

@api_view(['POST'])
def load_order(request):
    """Loads a new order from JSON and initializes it to 'Material' stage."""
    data = request.data
    customer_data = data["customer"]

    customer, _ = Customer.objects.get_or_create(
        name=customer_data["name"],
        email=customer_data["email"],
        phone=customer_data["phone"],
        address=customer_data["address"],
    )

    order, created = Order.objects.get_or_create(
        order_id=data["order_id"],
        defaults={
            "timestamp": parse_datetime(data["timestamp"]),
            "customer": customer,
            "total": data["total"],
            "current_status": "Material",
        }
    )

    if created:
        for item_data in data["items"]:
            Item.objects.create(
                name=item_data["name"],
                quantity=item_data["quantity"],
                price=item_data["price"],
                status="Material",
                order=order
            )

        for history in data["status_history"]:
            StatusHistory.objects.create(
                order=order,
                status=history["status"],
                timestamp=parse_datetime(history["timestamp"]),
                notes=history["notes"]
            )

    return Response({"message": "Order loaded successfully."}, status=201)


@api_view(['GET'])
def get_orders(request):
    """Returns a list of orders with basic details for dashboard display."""
    orders = Order.objects.all()
    data = []

    for order in orders:
        customer = Customer.objects.get(id=order.customer_id)
        items = Item.objects.filter(order_id=order.id)

        if not items.exists():
            continue

        order_dict = {
            "order_id": order.order_id,
            "customer": {
                "name": customer.name
            },
            "items": []
        }

        for item in items:
            order_dict["items"].append({
                "id": item.id,
                "name": item.name,
                "quantity": item.quantity,
                "status": item.status
            })

        data.append(order_dict)

    return JsonResponse(data, safe=False)


@api_view(['POST'])
def update_item(request):
    """Updates an item's stage and sends an email to the next stage handler."""
    try:
        item_id = request.data.get('item_id')
        next_stage = request.data.get('next_stage')
        notes = request.data.get('notes')

        item = Item.objects.get(id=item_id)
        item.status = next_stage
        item.save()

        order = item.order
        stage_email = STAGE_EMAILS.get(next_stage)

        if not stage_email:
            return Response({"error": f"No email defined for stage: {next_stage}"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ SendGrid email logic
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=stage_email,
            subject=f"Supply Chain Notification: Order {order.order_id} → {next_stage}",
            plain_text_content=f"""Hello,

The following item has reached your stage in the supply chain:

Order ID: {order.order_id}
Customer Name: {order.customer.name}
Item: {item.name}
Quantity: {item.quantity}
Next Stage: {next_stage}
Notes: {notes or 'None'}

Please proceed with your processing.

Thank you,
Supply Chain System
"""
        )

        response = sg.send(message)
        print("✅ Email sent:", response.status_code)

        return Response({"message": f"Item moved to {next_stage}. Email sent to {stage_email}."}, status=status.HTTP_200_OK)

    except Item.DoesNotExist:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
