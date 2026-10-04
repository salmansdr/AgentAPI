"""FastAPI Order Service for order details and customer order lookups."""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Order Service", version="0.1.0")

ORDER_DETAILS = [
    {
        "orderId": "order-1001",
        "customerId": "cust-001",
        "status": "shipped",
        "total": 129.99,
        "items": ["wireless keyboard", "mouse"],
    },
    {
        "orderId": "order-1002",
        "customerId": "cust-002",
        "status": "processing",
        "total": 79.50,
        "items": ["usb-c dock"],
    },
    {
        "orderId": "order-1003",
        "customerId": "cust-003",
        "status": "processing",
        "total": 89.50,
        "items": ["usb-c dock"],
     },
      {
             "orderId": "order-1004",
             "customerId": "cust-004",
             "status": "processing",
             "total": 99.50,
             "items": ["wireless keyboard","usb-c dock"],
          },
]





@app.get("/orders")
def get_order_details() -> list[dict[str, object]]:
    """Return all order details."""
    return ORDER_DETAILS


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> dict[str, object]:
    """Return one order by order identifier."""
    for order in ORDER_DETAILS:
        if order["orderId"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: str) -> list[dict[str, object]]:
    """Return all orders for a specific customer."""
    return [
        order for order in ORDER_DETAILS if order["customerId"] == customer_id
    ]