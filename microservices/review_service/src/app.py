from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import threading
import json
import pika
from config.config import Config

load_dotenv()

app = FastAPI(title="Review Service")
config = Config()

# RabbitMQ Connection
credentials = pika.PlainCredentials(
    config.RABBITMQ_USER,
    config.RABBITMQ_PASS
)

params = pika.ConnectionParameters(
    host=config.RABBITMQ_HOST,
    port=config.RABBITMQ_PORT,
    virtual_host=config.RABBITMQ_VHOST,
    credentials=credentials
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare exchange (MUST match payment_service)
channel.exchange_declare(
    exchange=config.PAYMENT_EXCHANGE,   # "payment_exchange"
    exchange_type="topic",
    durable=True
)

# Declare queue for receiving payment events
queue = "review_payment_q"
channel.queue_declare(queue=queue, durable=True)

# Bind: receive all events where routing key begins with "payment."
channel.queue_bind(
    queue=queue,
    exchange=config.PAYMENT_EXCHANGE,
    routing_key="payment.*"
)

class ReviewCreate(BaseModel):
    userId: str
    text: str

@app.get("/health")
def health():
    return {"ok": True, "service": "review-service"}

@app.post("/reviews")
def create_review(data: ReviewCreate):
    return {"ok": True, "reviewId": "rev_" + data.userId}

def handle_messages():
    def callback(ch, method, properties, body):
        event = json.loads(body)
        print("[review_service] Received Payment Event:", event)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=False
    )

    channel.start_consuming()

threading.Thread(target=handle_messages, daemon=True).start()