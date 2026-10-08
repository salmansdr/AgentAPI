import os
from db import get_db_connection

USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

STATIC_ORDERS = [
    {"orderId":1,"orderDate":"05/10/2026 11:18","status":"shipped","quantity":1,"total":129.99,"customerId":1,"firstName":"Syed","lastName":"Salman","email":"syed@example.com","phone":"9876543210","address":"Kolkata","productId":1,"productName":"Wireless Keyboard","productDescription":"Compact Bluetooth keyboard","price":129.99},
    {"orderId":2,"orderDate":"02/10/2026 11:18","status":"processing","quantity":1,"total":79.50,"customerId":2,"firstName":"Amit","lastName":"Sharma","email":"amit.sharma@example.com","phone":"9123456780","address":"Delhi","productId":2,"productName":"USB-C Dock","productDescription":"Multiport docking station","price":79.50},
    {"orderId":3,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":79.50,"customerId":3,"firstName":"Priya","lastName":"Das","email":"priya.das@example.com","phone":"9988776655","address":"Mumbai","productId":2,"productName":"USB-C Dock","productDescription":"Multiport docking station","price":79.50},
    {"orderId":4,"orderDate":"03/10/2026 11:18","status":"shipped","quantity":2,"total":50.00,"customerId":4,"firstName":"Ravi","lastName":"Kumar","email":"ravi.kumar@example.com","phone":"9112233445","address":"Chennai","productId":3,"productName":"Mouse","productDescription":"Wireless optical mouse","price":25.00},
    {"orderId":5,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":45.00,"customerId":5,"firstName":"Sneha","lastName":"Roy","email":"sneha.roy@example.com","phone":"9001122334","address":"Bangalore","productId":4,"productName":"Laptop Stand","productDescription":"Adjustable aluminum stand","price":45.00},
    {"orderId":6,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":199.99,"customerId":6,"firstName":"Arjun","lastName":"Mehta","email":"arjun.mehta@example.com","phone":"9223344556","address":"Hyderabad","productId":5,"productName":"Headphones","productDescription":"Noise-cancelling headphones","price":199.99},
    {"orderId":7,"orderDate":"05/11/2026 11:18","status":"processing","quantity":1,"total":59.99,"customerId":1,"firstName":"Syed","lastName":"Salman","email":"syed@example.com","phone":"9876543210","address":"Kolkata","productId":6,"productName":"Webcam","productDescription":"HD USB webcam","price":59.99},
    {"orderId":8,"orderDate":"05/12/2026 11:18","status":"shipped","quantity":1,"total":129.99,"customerId":2,"firstName":"Amit","lastName":"Sharma","email":"amit.sharma@example.com","phone":"9123456780","address":"Delhi","productId":1,"productName":"Wireless Keyboard","productDescription":"Compact Bluetooth keyboard","price":129.99},
    {"orderId":9,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":199.99,"customerId":3,"firstName":"Priya","lastName":"Das","email":"priya.das@example.com","phone":"9988776655","address":"Mumbai","productId":5,"productName":"Headphones","productDescription":"Noise-cancelling headphones","price":199.99},
    {"orderId":10,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":79.50,"customerId":4,"firstName":"Ravi","lastName":"Kumar","email":"ravi.kumar@example.com","phone":"9112233445","address":"Chennai","productId":2,"productName":"USB-C Dock","productDescription":"Multiport docking station","price":79.50},
    {"orderId":11,"orderDate":"05/10/2026 11:18","status":"processing","quantity":1,"total":79.50,"customerId":4,"firstName":"Syed","lastName":"Salman","email":"ravi.kumar@example.com","phone":"9112233445","address":"Chennai","productId":2,"productName":"USB-C Dock","productDescription":"Multiport docking station","price":79.50}
]


def get_orders(customer_id=None, order_id=None):
    if not USE_DATABASE:
        if order_id:
            return [o for o in STATIC_ORDERS if o["orderId"] == order_id]
        if customer_id:
            return [o for o in STATIC_ORDERS if o["customerId"] == customer_id]
        return STATIC_ORDERS

    conn = get_db_connection()
    cursor = conn.cursor()
    if customer_id:
        cursor.execute("EXEC GetCustomerOrderDetails @CustomerID = ?", customer_id)
    elif order_id:
        cursor.execute("EXEC GetCustomerOrderDetails @OrderID = ?", order_id)
    else:
        cursor.execute("EXEC GetCustomerOrderDetails")

    rows = cursor.fetchall()
    return [
        {
            "orderId": row.OrderID,
            "customerId": row.CustomerID,
            "status": row.Status,
            "total": float(row.Total),
            "items": [row.ProductName],
            "customerName": f"{row.FirstName} {row.LastName}",
            "email": row.Email,
            "phone": row.Phone,
            "address": row.Address,
            "productId": row.ProductID,
            "productDescription": row.ProductDescription,
            "price": float(row.Price),
            "orderDate": str(row.OrderDate),
        }
        for row in rows
    ]
