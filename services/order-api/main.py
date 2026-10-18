from fastapi import FastAPI, HTTPException
import customer_service, product_service, order_service,project_estimation,reconciliation

app = FastAPI(title="Ecommerce API", version="1.0.0")



@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/customers")
def get_customers():
    return customer_service.get_all_customers()

@app.get("/products")
def get_products():
    return product_service.get_all_products()

@app.get("/orders")
def get_orders(customer_id: int = None, order_id: int = None):
    return order_service.get_orders(customer_id=customer_id, order_id=order_id)

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    orders = order_service.get_orders(order_id=order_id)
    if orders:
        return orders[0]
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: int):
    return order_service.get_orders(customer_id=customer_id)

@app.get("/project-estimation/{estimation_id}")
def estimation(estimation_id: str):
    return project_estimation.get_estimation(estimation_id)

@app.get("/reconcile")
def reconcile():
    result = reconciliation.reconcile()   # call your reconciliation function
    print(result["ai_explanation"])
    return result["ai_explanation"]                        # still return JSON response to API caller


