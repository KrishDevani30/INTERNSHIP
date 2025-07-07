import os
import json
import logging
from django.apps import AppConfig
from django.utils.dateparse import parse_datetime

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from orders.models import Order, Customer, Item, StatusHistory

        import_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'imports')
        os.makedirs(import_dir, exist_ok=True)

        processed_file_path = os.path.join(import_dir, 'processed_files.txt')
        processed_files = set()

        if os.path.exists(processed_file_path):
            with open(processed_file_path, 'r') as f:
                processed_files = set(line.strip() for line in f)

        new_processed = []

        for filename in os.listdir(import_dir):
            if not filename.endswith(".json") or filename in processed_files:
                continue

            filepath = os.path.join(import_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    raw = f.read()
                    data = json.loads(raw)

                if isinstance(data, dict):
                    data = [data]  # Wrap single object in a list

                if not isinstance(data, list):
                    logging.error(f"❌ File {filename} does not contain a valid list of orders.")
                    continue

                for entry in data:
                    if not isinstance(entry, dict):
                        logging.warning(f"⚠️ Skipping malformed entry in {filename}: {entry}")
                        continue

                    order_id = entry.get("order_id")
                    if not order_id:
                        logging.warning(f"⚠️ Missing order_id in {filename} entry: {entry}")
                        continue

                    if Order.objects.filter(order_id=order_id).exists():
                        logging.info(f"ℹ️ Order {order_id} already exists. Skipping.")
                        continue

                    customer_data = entry.get("customer", {})
                    customer, _ = Customer.objects.get_or_create(
                        name=customer_data.get("name", ""),
                        email=customer_data.get("email", ""),
                        phone=customer_data.get("phone", ""),
                        address=customer_data.get("address", ""),
                    )

                    order = Order.objects.create(
                        order_id=order_id,
                        timestamp=parse_datetime(entry.get("timestamp", "")),
                        customer=customer,
                        total=entry.get("total", 0.0),
                        current_status=entry.get("current_status", "Material")
                    )

                    for item in entry.get("items", []):
                        if not isinstance(item, dict):
                            continue
                        Item.objects.create(
                            order=order,
                            name=item.get("name", ""),
                            quantity=item.get("quantity", 0),
                            price=item.get("price", 0.0),
                            status=item.get("status", "Material")
                        )

                    for history in entry.get("status_history", []):
                        if not isinstance(history, dict):
                            continue
                        StatusHistory.objects.create(
                            order=order,
                            status=history.get("status", "Material"),
                            timestamp=parse_datetime(history.get("timestamp", "")),
                            notes=history.get("notes", "")
                        )

                    logging.info(f"✅ Order {order_id} imported from {filename}")

                new_processed.append(filename)

            except Exception as e:
                logging.error(f"❌ Failed to load {filename}: {e}\nRaw content:\n{raw}")

        if new_processed:
            with open(processed_file_path, 'a') as f:
                for fname in new_processed:
                    f.write(fname + "\n")
