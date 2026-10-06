import os
from db import get_db_connection

USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

STATIC_PRODUCTS = [
    {"productId":1,"name":"Wireless Keyboard","description":"Compact Bluetooth keyboard","price":129.99,"stock":50},
    {"productId":2,"name":"USB-C Dock","description":"Multiport docking station","price":79.50,"stock":30},
    {"productId":3,"name":"Mouse","description":"Wireless optical mouse","price":25.00,"stock":100},
    {"productId":4,"name":"Laptop Stand","description":"Adjustable aluminum stand","price":45.00,"stock":40},
    {"productId":5,"name":"Headphones","description":"Noise-cancelling headphones","price":199.99,"stock":20},
    {"productId":6,"name":"Webcam","description":"HD USB webcam","price":59.99,"stock":25}
]


def get_all_products():
    if not USE_DATABASE:
        return STATIC_PRODUCTS

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, Name, Description, Price, Stock FROM Product")
    return [
        {
            "productId": row.ProductID,
            "name": row.Name,
            "description": row.Description,
            "price": float(row.Price),
            "stock": row.Stock,
        }
        for row in cursor.fetchall()
    ]
