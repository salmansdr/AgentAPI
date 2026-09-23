"""Azure Function that returns static customer details."""

import json

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CUSTOMERS = {
    "cust-001": {
        "customerId": "cust-001",
        "name": "Ava Patel",
        "email": "ava.patel@example.com",
        "phone": "+1-555-0101",
        "status": "active",
    },
    "cust-002": {
        "customerId": "cust-002",
        "name": "Liam Chen",
        "email": "liam.chen@example.com",
        "phone": "+1-555-0102",
        "status": "active",
    },
}


@app.route(route="customers", methods=["GET"])
def get_customers(req: func.HttpRequest) -> func.HttpResponse:
    """Return all static customer details."""
    return func.HttpResponse(
        json.dumps({"customers": list(CUSTOMERS.values())}),
        status_code=200,
        mimetype="application/json",
    )


@app.route(route="customers/{customer_id}", methods=["GET"])
def get_customer_details(req: func.HttpRequest) -> func.HttpResponse:
    """Return static customer details for the requested customer."""
    customer_id = req.route_params.get("customer_id", "")
    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return func.HttpResponse(
            json.dumps({"detail": "Customer not found"}),
            status_code=404,
            mimetype="application/json",
        )

    return func.HttpResponse(
        json.dumps({"customerDetails": customer}),
        status_code=200,
        mimetype="application/json",
    )