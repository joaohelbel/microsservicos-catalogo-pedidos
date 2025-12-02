import os
import json
import time
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])

app = FastAPI(title="Order Service", version="1.0.0")

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

@app.middleware("http")
async def metrics_middleware(request, call_next):
    endpoint = request.url.path
    method = request.method
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        response = await call_next(request)
    return response

@app.get("/health", tags=["health"])
def health():
    try:
        r.ping()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/orders", tags=["orders"])
def create_order(order: OrderCreate):
    payload = {
        "product_id": order.product_id,
        "quantity": order.quantity,
        "created_at": time.time(),
    }
    r.lpush(QUEUE_NAME, json.dumps(payload))
    return {"status": "queued", "order": payload}
