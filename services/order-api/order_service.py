import os
from db import get_db_connection

USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

STATIC_ORDERS = [
    {"orderId": 1001, "customerId": 1, "status": "shipped", "total": 129.99, "items": ["Wireless Keyboard"]},
    {"orderId": 1002, "customerId": 2, "status": "processing", "total": 79.50, "items": ["USB-C Dock"]},
    {"orderId": 1003, "customerId": 3, "status": "processing", "total": 25.00, "items": ["Mouse"]},
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
