from fastapi import FastAPI

app=FastAPI()
@app.get('/')
def calculate_item_cost(price: float, quantity: int) -> float:
    if price <= 0 or quantity <= 0:
        raise ValueError("Price and quantity must be positive")
    return price * quantity


