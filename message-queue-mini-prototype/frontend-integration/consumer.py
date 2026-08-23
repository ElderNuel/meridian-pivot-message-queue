import pika
import json
import time
import requests # <--- Add this import

def callback(ch, method, properties, body):
    data = json.loads(body)
    message_content = data.get("message")
    
    print(f" [x] Received '{message_content}'")
    
    # Simulate work (e.g., waiting for a printer)
    time.sleep(3) 
    
    print(f" [x] Finished processing '{message_content}'")
    
    # Acknowledge the message so RabbitMQ removes it from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # --- NEW: Tell the FastAPI server to update the frontend ---
    try:
        requests.post("http://127.0.0.1:8000/notify-frontend", json={"payload": message_content})
    except requests.exceptions.RequestException:
        print("[!] Could not notify frontend.")

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='assignment_1_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='assignment_1_queue', on_message_callback=callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()