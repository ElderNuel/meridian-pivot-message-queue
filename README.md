# Message Queue Mini-Prototype

**Author:** Emmanuel Chijinkem Ukah  
**Project:** The Meridian Pivot — Assignment 1 (Power Learn Project)  
**Assigned Tool:** Message Queue — RabbitMQ via Python/Pika

A mini-prototype demonstrating a **producer-consumer message queue architecture** using Python and RabbitMQ. The prototype simulates asynchronous inventory-processing requests and demonstrates how messages can remain safely queued when a worker is temporarily unavailable.

---

## 📌 Project Overview

This project demonstrates a simple asynchronous workflow:

```text
                 ┌──────────────────┐
                 │   Producer/API   │
                 │  producer.py     │
                 └────────┬─────────┘
                          │
                          │ Publish message
                          ▼
                 ┌──────────────────┐
                 │    RabbitMQ      │
                 │                  │
                 │ inventory_sync   │
                 └────────┬─────────┘
                          │
                          │ Deliver message
                          ▼
                 ┌──────────────────┐
                 │    Consumer      │
                 │  consumer.py     │
                 │  Background      │
                 │     Worker       │
                 └────────┬─────────┘
                          │
                          ▼
                  Process inventory
                  request & ACK
```

The **producer** creates an inventory request and sends it to RabbitMQ.

RabbitMQ stores the message in the `inventory_sync` queue until a consumer is available.

The **consumer** receives the message, processes it, and sends an acknowledgment (`ACK`) after successful processing.

This architecture demonstrates:

- Asynchronous processing
- Message queuing
- Producer-consumer architecture
- Background workers
- Message persistence
- Manual acknowledgment
- Basic fault tolerance and message resiliency

---

# 📁 Project Structure

The repository should contain files similar to:

```text
message-queue-mini-prototype/
│
├── producer.py
├── consumer.py
├── README.md
└── requirements.txt
```

### `producer.py`

Simulates an API endpoint or application component that publishes inventory requests to RabbitMQ.

### `consumer.py`

Acts as a background worker that listens for messages and processes inventory requests.

### `README.md`

Contains the project documentation and instructions for running and testing the prototype.

### `requirements.txt`

Contains the Python dependencies required by the project.

---

# 🛠️ Prerequisites

Before running the prototype, install the following:

### 1. Python

Install **Python 3.8 or later**.

Verify your installation:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### 2. Docker Desktop

Install Docker Desktop if you want to run RabbitMQ in a container.

Verify Docker:

```bash
docker --version
```

Docker Desktop must be **running** before starting the RabbitMQ container.

---

### 3. Git Bash / Terminal

You need a terminal for running the Python scripts and Docker commands.

Windows users can use:

- Git Bash
- Command Prompt
- PowerShell
- Windows Terminal

---

# 🚀 Step 1 — Clone or Download the Repository

If the project is hosted on GitHub, clone it with:

```bash
git clone https://github.com/ElderNuel/meridian-pivot-message-queue.git
```

Then enter the project directory:

```bash
cd message-queue-mini-prototype
```

If you downloaded the repository as a ZIP file, extract it and open your terminal inside the project folder.

Verify the files:

```bash
ls
```

On Windows Command Prompt:

```cmd
dir
```

You should see:

```text
producer.py
consumer.py
README.md
requirements.txt
```

---

# 🐍 Step 2 — Create a Python Virtual Environment

Creating a virtual environment keeps the project's Python dependencies isolated.

Run:

```bash
python -m venv venv
```

Activate it on **Windows Git Bash**:

```bash
source venv/Scripts/activate
```

On **Windows Command Prompt**:

```cmd
venv\Scripts\activate
```

On **PowerShell**:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source venv/bin/activate
```

After activation, your terminal should display something similar to:

```text
(venv)
```

---

# 📦 Step 3 — Install Python Dependencies

Install Pika:

```bash
pip install pika
```

Or, if the repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

Verify the installation:

```bash
pip show pika
```

---

# 🐇 Step 4 — Start RabbitMQ

The easiest way to run RabbitMQ locally is with Docker.

Run:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### What the ports mean

| Port | Purpose |
|---|---|
| `5672` | RabbitMQ AMQP communication |
| `15672` | RabbitMQ Management Web Interface |

The terminal will display RabbitMQ startup logs.

Wait until RabbitMQ has finished starting.

### Important

**Do not close this terminal** while testing the application.

If you close it, the RabbitMQ container will stop.

---

# 🖥️ Step 5 — Open RabbitMQ Management Dashboard

Once RabbitMQ is running, open:

**http://localhost:15672**

Log in with:

```text
Username: guest
Password: guest
```

The RabbitMQ Management Dashboard allows you to monitor:

- Connections
- Channels
- Exchanges
- Queues
- Message rates
- Consumers
- Message counts

The `inventory_sync` queue should appear after the producer or consumer creates it.

---

# 👷 Step 6 — Start the Consumer

Open a **second terminal window**.

Navigate to the project directory:

```bash
cd message-queue-mini-prototype
```

If necessary, activate the virtual environment again.

Then run:

```bash
python consumer.py
```

Expected output:

```text
[*] Waiting for messages. To exit press CTRL+C
```

The consumer is now acting as a background worker.

It will remain idle until a message is placed in the queue.

**Do not close this terminal.**

---

# 📤 Step 7 — Run the Producer

Open a **third terminal window**.

Navigate to the project directory:

```bash
cd message-queue-mini-prototype
```

Activate the virtual environment if necessary.

Run:

```bash
python producer.py
```

The producer should publish an inventory request to RabbitMQ.

Expected output will be similar to:

```text
[x] Sent {'item_id': 'SKU-9942', 'action': 'check_stock', 'timestamp': '2026-08-18T05:25:08Z'}
```

The exact timestamp will depend on when the script is executed.

---

# 🔄 Step 8 — Observe Message Processing

Return to the terminal running `consumer.py`.

The consumer should receive and process the message.

Expected output:

```text
[x] Received request for SKU-9942
[x] Stock check complete.
```

The complete flow is:

```text
producer.py
     │
     │  Publish message
     ▼
RabbitMQ
     │
     │  Deliver message
     ▼
consumer.py
     │
     │  Process request
     ▼
ACK
```

Once the consumer acknowledges the message, RabbitMQ removes the successfully processed message from the queue.

---

# 🧪 Step 9 — Verify the Queue in RabbitMQ

Open:

```text
http://localhost:15672
```

Navigate to:

```text
Queues and Streams
```

Look for:

```text
inventory_sync
```

Click the queue to inspect its details.

You should be able to see information such as:

- Number of messages
- Ready messages
- Unacknowledged messages
- Consumers
- Message rates

### Understanding the message counts

**Ready**

Messages waiting in the queue that have not yet been delivered to a consumer.

**Unacknowledged**

Messages that have been delivered to a consumer but have not yet received an acknowledgment.

**Total**

The total number of messages currently represented in the queue state.

---

# 🧪 Step 10 — Test Multiple Messages

You can test the queue with multiple producer requests.

With `consumer.py` running, execute:

```bash
python producer.py
```

multiple times.

For example:

```bash
python producer.py
python producer.py
python producer.py
```

The consumer should receive the messages individually.

You should see output similar to:

```text
[x] Received request for SKU-9942
[x] Stock check complete.

[x] Received request for SKU-9942
[x] Stock check complete.

[x] Received request for SKU-9942
[x] Stock check complete.
```

This demonstrates that RabbitMQ can handle multiple messages through the same queue.

---

# 💾 Step 11 — Test Message Persistence

This test verifies that messages remain available when the consumer is offline.

### 11.1 Stop the Consumer

Go to the terminal running:

```bash
python consumer.py
```

Press:

```text
CTRL+C
```

The consumer should stop.

RabbitMQ itself should remain running in the Docker terminal.

---

### 11.2 Send Messages While the Consumer Is Offline

From another terminal, run:

```bash
python producer.py
```

Run it three times:

```bash
python producer.py
python producer.py
python producer.py
```

Because no consumer is currently processing the queue, the messages should remain waiting in RabbitMQ.

---

### 11.3 Check RabbitMQ

Open:

```text
http://localhost:15672
```

Navigate to:

```text
Queues and Streams
→ inventory_sync
```

You should see messages waiting to be consumed.

The **Ready** message count should increase.

---

### 11.4 Restart the Consumer

Start the consumer again:

```bash
python consumer.py
```

It should immediately begin processing the waiting messages.

Expected output:

```text
[*] Waiting for messages. To exit press CTRL+C
[x] Received request for SKU-9942
[x] Stock check complete.
[x] Received request for SKU-9942
[x] Stock check complete.
[x] Received request for SKU-9942
[x] Stock check complete.
```

### What this proves

This demonstrates that the queue can temporarily decouple the producer from the consumer.

The producer does not have to wait for the worker to be available before submitting the task.

---

# 🛡️ Step 12 — Test Manual Acknowledgment and Message Recovery

The consumer should acknowledge a message **only after successful processing**.

This provides protection against losing a message when a worker fails during processing.

## Temporary Test Modification

Open:

```text
consumer.py
```

Find the section where the message is acknowledged:

```python
ch.basic_ack(delivery_tag=method.delivery_tag)
```

Temporarily add:

```python
import time
```

and add a delay immediately before the acknowledgment:

```python
time.sleep(10)
ch.basic_ack(delivery_tag=method.delivery_tag)
```

The relevant flow should look conceptually like:

```python
# Process message
print(f"[x] Received request for {item_id}")

time.sleep(2)

print("[x] Stock check complete.")

# Temporary resiliency test
time.sleep(10)

# Acknowledge only after processing
ch.basic_ack(delivery_tag=method.delivery_tag)
```

---

## Run the Recovery Test

### 12.1 Start the Consumer

```bash
python consumer.py
```

### 12.2 Send a Message

From another terminal:

```bash
python producer.py
```

### 12.3 Interrupt the Consumer

When the consumer is inside the 10-second delay, press:

```text
CTRL+C
```

before it reaches:

```python
ch.basic_ack(...)
```

The worker will terminate before acknowledging the message.

### 12.4 Restart the Consumer

Start it again:

```bash
python consumer.py
```

RabbitMQ should redeliver the unacknowledged message.

The consumer should process it again.

---

# 🔍 Why Manual Acknowledgment Matters

Without proper acknowledgment handling, a worker could potentially fail after receiving a message and before completing the task.

The desired sequence is:

```text
Receive
   ↓
Process
   ↓
Complete successfully
   ↓
ACK
```

If the worker fails:

```text
Receive
   ↓
Process
   ↓
💥 Worker failure
```

RabbitMQ can make the unacknowledged message available for another consumer/restart, depending on the queue and consumer configuration.

This is an important property of message-based architectures because it helps prevent tasks from simply disappearing when a worker crashes.

---

# 🧹 Step 13 — Remove the Temporary Test Delay

After completing the resiliency test, remove:

```python
time.sleep(10)
```

Keep the normal processing delay, if it is part of the prototype.

Your production-style flow should return to:

```python
# Process message

# Acknowledge after successful processing
ch.basic_ack(delivery_tag=method.delivery_tag)
```

---

# 📊 Step 14 — Test the Complete Workflow

For a complete demonstration, use three terminals.

### Terminal 1 — RabbitMQ

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### Terminal 2 — Consumer

```bash
python consumer.py
```

Expected:

```text
[*] Waiting for messages. To exit press CTRL+C
```

### Terminal 3 — Producer

```bash
python producer.py
```

Expected:

```text
[x] Sent {'item_id': 'SKU-9942', 'action': 'check_stock', 'timestamp': '...'}
```

Consumer:

```text
[x] Received request for SKU-9942
[x] Stock check complete.
```

RabbitMQ Dashboard:

```text
inventory_sync
```

This confirms the complete producer → broker → consumer workflow.

---

# 🧪 Recommended Test Checklist

Use the following checklist when demonstrating the prototype.

- [ ] Python 3.8+ is installed
- [ ] Docker Desktop is running
- [ ] Project repository has been opened
- [ ] Python virtual environment has been created
- [ ] `pika` has been installed
- [ ] RabbitMQ Docker container is running
- [ ] RabbitMQ Management Dashboard opens at `http://localhost:15672`
- [ ] `consumer.py` starts successfully
- [ ] Producer successfully publishes a message
- [ ] Consumer receives the message
- [ ] Consumer processes the inventory request
- [ ] Consumer acknowledges the message
- [ ] `inventory_sync` appears in RabbitMQ
- [ ] Multiple messages can be queued
- [ ] Messages remain queued while the consumer is offline
- [ ] Queued messages are processed after restarting the consumer
- [ ] Manual acknowledgment recovery test succeeds
- [ ] Temporary 10-second test delay has been removed

---

# 🐛 Troubleshooting

## `ModuleNotFoundError: No module named 'pika'`

Install Pika:

```bash
pip install pika
```

If using a virtual environment, make sure it is activated first.

---

## Cannot connect to RabbitMQ

Check that the Docker container is running:

```bash
docker ps
```

You should see a container named:

```text
rabbitmq
```

If it is not running, start it again:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

---

## Port `5672` is already in use

Another RabbitMQ instance or application may already be using port `5672`.

Check running Docker containers:

```bash
docker ps
```

You can stop a conflicting container with:

```bash
docker stop <container-name-or-id>
```

Alternatively, change the host-side port mapping, for example:

```bash
-p 5673:5672
```

If you change the port, make sure the Python scripts connect to the corresponding port.

---

## Port `15672` is already in use

Another service may be using RabbitMQ's management port.

Check Docker containers:

```bash
docker ps
```

You can also change the host-side management port:

```bash
-p 15673:15672
```

Then access the dashboard through:

```text
http://localhost:15673
```

---

## RabbitMQ Dashboard Does Not Open

Confirm:

1. Docker Desktop is running.
2. The RabbitMQ container is running.
3. Port `15672` is exposed.
4. RabbitMQ has finished starting.

Check:

```bash
docker ps
```

Then inspect the logs:

```bash
docker logs rabbitmq
```

---

## Consumer Starts but Does Not Receive Messages

Check the following:

1. RabbitMQ is running.
2. Producer and consumer are connecting to the same RabbitMQ instance.
3. Both scripts use the same queue name.
4. The producer has actually been executed.
5. The `inventory_sync` queue exists in the RabbitMQ dashboard.

---

# 🧠 Key Concepts Demonstrated

## Producer

The producer creates and publishes a message.

```text
Application/API
      ↓
Producer
      ↓
RabbitMQ
```

In a real application, the producer could be:

- A REST API
- A web application
- An inventory management system
- A scheduled task

---

## Message Broker

RabbitMQ acts as the intermediary between the producer and consumer.

```text
Producer → RabbitMQ → Consumer
```

The producer and consumer do not have to operate at exactly the same time.

---

## Consumer

The consumer is a background worker that retrieves and processes queued tasks.

```text
RabbitMQ
   ↓
Consumer
   ↓
Business Logic
```

---

## Queue

The `inventory_sync` queue temporarily stores inventory-processing requests.

This allows messages to wait until a worker is ready to process them.

---

## Acknowledgment

The consumer sends an acknowledgment after successfully processing a message:

```python
ch.basic_ack(delivery_tag=method.delivery_tag)
```

This tells RabbitMQ that the message has been successfully handled.

---

# 🏗️ Real-World Application

Although this prototype uses a simple inventory check, the same architecture can be used for more complex systems.

For example:

```text
Customer Order
      ↓
Order API
      ↓
RabbitMQ
      ↓
Order Worker
      ↓
Inventory Service
      ↓
Database
```

Other possible applications include:

- Inventory synchronization
- Email processing
- Payment processing
- Notification systems
- Image/video processing
- Background report generation
- Order fulfillment
- Data synchronization between services
- Microservice communication

---

# 🔐 Important Note About Persistence

There are two related concepts when discussing RabbitMQ resiliency:

1. **Messages surviving while a consumer is offline**
2. **Messages and queues surviving a RabbitMQ broker restart**

This prototype's offline-consumer test demonstrates the first scenario.

For stronger broker-level durability, the application should also explicitly configure durable queues and persistent messages.

For example, a durable queue can be declared with:

```python
channel.queue_declare(queue='inventory_sync', durable=True)
```

And a persistent message can be published with:

```python
channel.basic_publish(
    exchange='',
    routing_key='inventory_sync',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)
```

These settings are important when building a production-grade RabbitMQ implementation because they address broker restart scenarios as well.

---

# 🔄 Complete Testing Sequence

For the simplest successful demonstration, follow this exact order:

```text
1. Start Docker Desktop
        ↓
2. Start RabbitMQ
        ↓
3. Open RabbitMQ Dashboard
        ↓
4. Start consumer.py
        ↓
5. Run producer.py
        ↓
6. Check consumer output
        ↓
7. Check inventory_sync queue
        ↓
8. Stop consumer
        ↓
9. Send 3 messages with producer.py
        ↓
10. Check queued messages
        ↓
11. Restart consumer.py
        ↓
12. Verify all 3 messages are processed
        ↓
13. Run manual ACK failure test
        ↓
14. Verify message redelivery
        ↓
15. Remove temporary test delay
```

---

# 📸 Evidence Captured for Assignment Submission

For the Power Learn Project assignment, useful evidence/screenshots include:

### Screenshot 1 — RabbitMQ Running

Show the terminal containing the RabbitMQ Docker container.

### Screenshot 2 — RabbitMQ Dashboard

Show:

```text
http://localhost:15672
```

with the RabbitMQ Management Dashboard open.

### Screenshot 3 — Queue

Show:

```text
inventory_sync
```

inside the **Queues and Streams** section.

### Screenshot 4 — Producer

Show the producer terminal with:

```text
[x] Sent {...}
```

### Screenshot 5 — Consumer

Show:

```text
[x] Received request for SKU-9942
[x] Stock check complete.
```

### Screenshot 6 — Message Persistence Test

Show messages waiting in the `inventory_sync` queue while the consumer is stopped.

### Screenshot 7 — Recovery Test

Show the consumer receiving the message again after the worker was interrupted before acknowledgment.

These screenshots provide visual evidence that the message queue was actually tested rather than only implemented.

---

# 🛑 Stopping the Prototype

When finished testing, stop the Python consumer with:

```text
CTRL+C
```

Then stop the RabbitMQ Docker container with:

```text
CTRL+C
```

Because the container was started with:

```bash
--rm
```

Docker will automatically remove the container after it stops.

You can verify that it is no longer running:

```bash
docker ps
```

---

# 📌 Summary

This mini-prototype demonstrates a basic but important asynchronous processing architecture:

```text
┌─────────────┐
│   Producer  │
│ producer.py │
└──────┬──────┘
       │
       │ Publish
       ▼
┌──────────────────┐
│     RabbitMQ     │
│                  │
│ inventory_sync   │
└────────┬─────────┘
         │
         │ Deliver
         ▼
┌──────────────┐
│   Consumer   │
│ consumer.py  │
└──────┬───────┘
       │
       │ Process
       ▼
┌──────────────┐
│     ACK      │
└──────────────┘
```

The prototype demonstrates how RabbitMQ can decouple message producers from background workers and provide a reliable mechanism for asynchronous task processing.

The most important tests are:

1. **Basic message delivery** — producer sends a message and consumer receives it.
2. **Multiple messages** — several requests can be placed on the queue.
3. **Consumer downtime** — messages remain queued while the worker is offline.
4. **Manual acknowledgment** — a message that is not acknowledged can be redelivered after a worker failure.
5. **RabbitMQ monitoring** — the Management Dashboard provides visibility into queues, consumers, and message states.

Together, these tests provide a practical demonstration of **message queuing, asynchronous processing, background workers, and message resiliency** using Python, Pika, RabbitMQ, and Docker.
