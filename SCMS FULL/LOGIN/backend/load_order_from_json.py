import requests
import os

# Path to the JSON order file (relative to this script)
ORDER_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../SHOP/orders/ORDER_20250618_114119.json'))

# API endpoint URL
API_URL = 'http://localhost:8000/api/load_order/'

# Read the JSON file
with open(ORDER_JSON_PATH, 'r') as f:
    order_data = f.read()

# Send POST request
response = requests.post(
    API_URL,
    data=order_data,
    headers={'Content-Type': 'application/json'}
)

print('Status code:', response.status_code)
print('Response:', response.text) 