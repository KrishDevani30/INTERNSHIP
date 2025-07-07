# Supply Chain Management System (SCMS)

A modern supply chain management system with a PyQt5 frontend.

## Features

- Modern and responsive UI design
- Product catalog with images and details
- Shopping cart functionality
- Order placement with customer details
- Order history tracking

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create an 'images' directory and add your product images:
```bash
mkdir images
```

3. Add product images to the 'images' directory with the following names:
- laptop.png
- phone.png
- tablet.png
- watch.png
- headphones.png

Image requirements:
- Recommended size: 500x500 pixels
- Format: PNG or JPG
- Background: Transparent or white
- If images are not found, the system will create placeholder images with product initials

4. Run the application:
```bash
python scms_frontend.py
```

## Product Images

You can customize product images by:

1. Using the default filenames (laptop.png, phone.png, etc.)
2. Or modifying the image filenames in the `load_products()` method in `scms_frontend.py`

Image Guidelines:
- Use high-quality product images
- Maintain consistent aspect ratios
- Prefer transparent backgrounds
- Keep file sizes reasonable (< 1MB per image)

## Styling

The application uses a modern, flat design with:
- Clean, minimalist interface
- Responsive layout
- Smooth animations and transitions
- Professional color scheme
- Clear typography

Colors used:
- Primary: #2ecc71 (Green)
- Secondary: #2c3e50 (Dark Blue)
- Background: #f5f5f5 (Light Gray)
- Text: #333333 (Dark Gray)
- Accent: #e1e1e1 (Border Gray)

## Orders

Orders are saved in the 'orders' directory with:
- Unique order ID
- Timestamp
- Customer details
- Product information
- Total amount

## Project Structure

- `scms_project/` - Django project settings
- `products/` - Django app for product and order management
- `scms_frontend.py` - PyQt5 frontend application
- `requirements.txt` - Python dependencies

## API Endpoints

- `GET /api/products/` - List all products
- `POST /api/orders/` - Create a new order

## Notes

- The frontend currently uses dummy product data
- Add product images to the media directory
- Customize the styling and layout as needed 