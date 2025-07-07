import json
import requests
import os

# Correct relative path
file_path = os.path.join("sample_data", "ORDER_20250612_114522.json")

# Load JSON and send to backend
with open(file_path, "r") as file:
    data = json.load(file)

response = requests.post("http://127.0.0.1:8000/api/load_order/", json=data)

if response.status_code == 201:
    print("Order loaded successfully!")
else:
    print("Failed to load order:", response.status_code)
    print(response.text)

