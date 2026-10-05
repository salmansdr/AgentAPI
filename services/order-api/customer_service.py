import os
from db import get_db_connection

USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

STATIC_CUSTOMERS = [
    {"customerId": 1, "firstName": "Syed", "lastName": "Salman", "email": "syed@example.com", "phone": "9876543210", "address": "Kolkata"},
    {"customerId": 2, "firstName": "Amit", "lastName": "Sharma", "email": "amit.sharma@example.com", "phone": "9123456780", "address": "Delhi"},
    {"customerId": 3, "firstName": "Priya", "lastName": "Das", "email": "priya.das@example.com", "phone": "9988776655", "address": "Mumbai"},
]

def get_all_customers():
    if not USE_DATABASE:
        return STATIC_CUSTOMERS

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID, FirstName, LastName, Email, Phone, Address FROM Customer")
    return [
        {
            "customerId": row.CustomerID,
            "firstName": row.FirstName,
            "lastName": row.LastName,
            "email": row.Email,
            "phone": row.Phone,
            "address": row.Address,
        }
        for row in cursor.fetchall()
    ]
