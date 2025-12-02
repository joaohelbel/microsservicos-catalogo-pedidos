import os
import json
import time
import redis
from prometheus_client import Counter, Histogram, start_http_server

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

ORDERS_PROCESSED = Counter("worker_orders_processed_total", "Total orders processed")
PROCESSING_TIME = Histogram("worker_order_processing_seconds", "Time to process an order")

def process_order(data: dict):
    # Simulação de processamento
    time.sleep(0.5)

def main():
    start_http_server(9100)
    print("Worker iniciado. Aguardando pedidos...")
    while True:
        _, item = r.brpop(QUEUE_NAME)
        payload = json.loads(item)
        with PROCESSING_TIME.time():
            process_order(payload)
        ORDERS_PROCESSED.inc()
        print("Pedido processado:", payload)

if __name__ == "__main__":
    main()
