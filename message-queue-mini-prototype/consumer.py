import pika
import json
import time

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(f" [x] Received request for {payload['item_id']}")
    
    # Simulate API polling and processing time
    time.sleep(2)
    
    print(" [x] Stock check complete.")
    # Acknowledge the message only after successful processing
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='inventory_sync', durable=True)

# Ensure the worker only gets one message at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='inventory_sync', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()