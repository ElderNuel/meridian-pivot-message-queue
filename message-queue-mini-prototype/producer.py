import pika
import json

# Establish connection to the local RabbitMQ broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a durable queue so messages survive broker restarts
channel.queue_declare(queue='inventory_sync', durable=True)

# Message payload representing an inventory query
message = {
    "item_id": "SKU-9942",
    "action": "check_stock",
    "timestamp": "2026-08-18T05:25:08Z"
}

# Publish message to the queue
channel.basic_publish(
    exchange='',
    routing_key='inventory_sync',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    )
)

print(f" [x] Sent {message}")
connection.close()