from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import CustomUser, DeleteLog, Product, Order, OrderItem, OrderStatusHistory
import json
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import datetime
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.dateparse import parse_datetime
import sendgrid
from sendgrid.helpers.mail import Mail
import os

# 🔐 Configure SendGrid API key and sender email here
SENDGRID_API_KEY = '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'  # Replace this with your actual SendGrid API key
SENDER_EMAIL = 'kingisright67@gmail.com'  # This must be verified in SendGrid

# 🔧 Stage-wise responsible person email mapping
STAGE_EMAILS = {
    'Material': 'yashbharvada4@gmail.com',
    'Manufacturing': 'gabanidj@gmail.com',
    'Packaging': 'princediyora05@gmail.com',
    'Dispatch': 'krrishmiraj12345@gmail.com',
    'Completed': 'kingisright67@gmail.com',
}

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'user')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = CustomUser.objects.create_user(username=username, password=password, role=role)
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            # Special handling for admin user
            if username == 'admin' and password == 'admin':
                return JsonResponse({
                    'message': 'Login successful',
                    'username': 'admin',
                    'role': 'admin'
                }, status=200)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'username': user.username,
                    'role': user.role
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        try:
            logout(request)
            return JsonResponse({'message': 'Logout successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_users(request):
    if request.method == 'GET':
        try:
            users = CustomUser.objects.all()
            user_list = [{'username': user.username, 'role': user.role} for user in users]
            return JsonResponse(user_list, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_user(request, username):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            reason = data.get('reason')
            deleted_by = data.get('deleted_by')
            
            if not reason:
                return JsonResponse({'error': 'Delete reason is required'}, status=400)
            
            user = CustomUser.objects.get(username=username)
            user_role = user.role
            
            # Create delete log before deleting user
            DeleteLog.objects.create(
                deleted_username=username,
                deleted_role=user_role,
                reason=reason,
                deleted_by=deleted_by
            )
            
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_products(request):
    """Get all products"""
    products = Product.objects.all()
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock': product.stock,
            'image_url': product.image_url
        })
    return JsonResponse({'products': products_data})

@csrf_exempt
@login_required
def create_order(request):
    """Create a new order"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        
        if not items:
            return JsonResponse({'error': 'No items in order'}, status=400)
        
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                order_id=str(uuid.uuid4()),
                customer=request.user,
                status='pending'
            )
            
            total_amount = 0
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                
                if product.stock < quantity:
                    raise ValueError(f'Not enough stock for {product.name}')
                
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                # Update stock
                product.stock -= quantity
                product.save()
                
                total_amount += float(product.price) * quantity
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            
            # Create status history
            OrderStatusHistory.objects.create(
                order=order,
                status='pending',
                notes='Order created'
            )
            
            return JsonResponse({
                'message': 'Order created successfully',
                'order_id': order.order_id
            })
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_user_orders(request):
    """Get orders for the current user"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    orders_data = []
    
    for order in orders:
        items = []
        for item in order.orderitem_set.all():
            items.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price)
            })
        
        orders_data.append({
            'order_id': order.order_id,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'created_at': order.created_at.isoformat(),
            'items': items
        })
    
    return JsonResponse({'orders': orders_data})

@csrf_exempt
@login_required
def add_product(request):
    """Add a new product (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        required_fields = ['name', 'description', 'price', 'stock']
        
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            image_url=data.get('image_url', '')
        )
        
        return JsonResponse({
            'message': 'Product added successfully',
            'product_id': product.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def update_order_status(request, order_id):
    """Update order status (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        order = Order.objects.get(order_id=order_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if not new_status:
            return JsonResponse({'error': 'Status is required'}, status=400)
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        order.status = new_status
        order.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            notes=data.get('notes', '')
        )
        
        return JsonResponse({'message': 'Order status updated successfully'})
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def load_order(request):
    """Loads a new order from JSON and initializes it to 'Material' stage."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        customer_data = data["customer"]

        # Try to get existing user first
        try:
            customer = CustomUser.objects.get(username=customer_data["name"])
        except CustomUser.DoesNotExist:
            # If user doesn't exist, create new one
            customer = CustomUser.objects.create(
                username=customer_data["name"],
                email=customer_data["email"],
                role='user',
                password=make_password(str(uuid.uuid4()))  # Generate random password
            )

        order = Order.objects.create(
            order_id=data["order_id"],
            customer=customer,
            total_amount=data["total"],
            status="Material"
        )

        for item_data in data["items"]:
            # Try to get the product, or create it if it doesn't exist
            try:
                product = Product.objects.get(name=item_data["name"])
            except Product.DoesNotExist:
                product = Product.objects.create(
                    name=item_data["name"],
                    description="Auto-created from order import",
                    price=item_data["price"],
                    image="",  # You can set a default or leave blank
                    stock=100  # Default stock
                )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data["quantity"],
                price=item_data["price"],
                status="Material"
            )

        OrderStatusHistory.objects.create(
            order=order,
            status="Material",
            notes="Order created and initialized"
        )

        return JsonResponse({"message": "Order loaded successfully."}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def get_orders(request):
    """Returns a list of orders with items filtered by item status (stage)."""
    try:
        from .models import Order, OrderItem

        status_filter = request.GET.get('status')
        orders_data = []

        for order in Order.objects.all():
            # Only include items in the requested stage
            if status_filter:
                items_qs = order.items.filter(status=status_filter)
            else:
                items_qs = order.items.all()

            items = []
            for item in items_qs:
                items.append({
                    "id": item.id,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "status": item.status,
                })

            # Only include orders that have at least one item in this stage
            if items:
                orders_data.append({
                    "order_id": order.order_id,
                    "customer": {
                        "name": order.customer.username,
                        "email": order.customer.email,
                    },
                    "items": items,
                    "total_amount": float(order.total_amount),
                    "status": order.status,
                    "created_at": order.created_at.isoformat(),
                    "status_history": [
                        {
                            "status": h.status,
                            "notes": h.notes,
                            "created_at": h.created_at.isoformat(),
                        }
                        for h in order.status_history.all()
                    ]
                })
        return JsonResponse(orders_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def update_item(request):
    """Updates an item's stage and sends an email to the next stage handler using SendGrid."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        next_stage = data.get('next_stage')
        notes = data.get('notes')

        # Validate input
        if not item_id or not next_stage:
            return JsonResponse({'error': 'item_id and next_stage are required'}, status=400)

        item = OrderItem.objects.get(id=item_id)
        item.status = next_stage
        item.save()

        order = item.order

        # Update JSON file if item is completed
        if next_stage == "Completed":
            order_json_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '../../../SHOP/orders', f"{order.order_id}.json")
            )
            if not os.path.exists(order_json_path):
                order_json_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '../../../SHOP/orders', f"ORDER{order.order_id}.json")
                )
            if os.path.exists(order_json_path):
                try:
                    with open(order_json_path, 'r') as f:
                        order_data = json.load(f)
                    order_data['status'] = 'Completed'
                    with open(order_json_path, 'w') as f:
                        json.dump(order_data, f, indent=2)
                except Exception as e:
                    print(f"Warning: Could not update order JSON status: {e}")

        # Add status history
        OrderStatusHistory.objects.create(
            order=order,
            status=next_stage,
            notes=notes or f"Item moved to {next_stage}"
        )

        # ✅ Send Email via SendGrid
        from django.conf import settings

        stage_email = settings.STAGE_EMAILS.get(next_stage)
        sender_email = settings.SENDER_EMAIL
        sendgrid_api_key = settings.SENDGRID_API_KEY

        if not all([stage_email, sender_email, sendgrid_api_key]):
            print("⚠ Email config is incomplete.")
            return JsonResponse({
                "message": f"Item moved to {next_stage}. But email not sent due to missing settings."
            }, status=200)

        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        message = Mail(
            from_email=sender_email,
            to_emails=stage_email,
            subject=f"Supply Chain Notification: Order {order.order_id} → {next_stage}",
            plain_text_content=f"""Hello,

The following item has reached your stage in the supply chain:

Order ID: {order.order_id}
Customer Name: {order.customer.username}
Item: {item.product.name}
Quantity: {item.quantity}
Next Stage: {next_stage}
Notes: {notes or 'None'}

Please proceed with your processing.

Thank you,
Supply Chain System
"""
        )
        response = sg.send(message)
        print(f"✅ Email sent to {stage_email}: Status {response.status_code}")
        return JsonResponse({"message": f"Item moved to {next_stage}. Email sent to {stage_email}."}, status=200)

    except OrderItem.DoesNotExist:
        return JsonResponse({"error": "Item not found."}, status=404)
    except Exception as e:
        print("❌ Exception in update_item:", e)
        return JsonResponse({"error": str(e)}, status=400)