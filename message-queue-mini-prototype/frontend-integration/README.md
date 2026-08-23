# Real-Time Message Queue Prototype — Frontend (Assignment 1)

**Author:** Emmanuel Chijinkem Ukah  
**Project:** Power Learn Project — Solo Reconnaissance Phase  
**Component:** Frontend (`index.html`)

This repository contains the frontend component of a full-stack, real-time message queue prototype built with **HTML, CSS, and vanilla JavaScript**.

The frontend provides a lightweight user interface for submitting text-based tasks to a FastAPI backend through a standard HTTP `POST` request. It also maintains a persistent **WebSocket** connection to receive real-time notifications when a background worker has finished processing each queued task.

The frontend does **not** process the queued task itself. Instead, it demonstrates the client-side portion of an asynchronous architecture:

**Browser → FastAPI → RabbitMQ → Background Worker → FastAPI WebSocket → Browser**

---

## 📌 What This Frontend Does

The `index.html` file performs the following functions:

1. Provides a text input where a user can enter a task or message.
2. Sends the entered message to the FastAPI backend using an HTTP `POST` request.
3. Displays immediate feedback when the message has been accepted by the backend.
4. Establishes a WebSocket connection with the FastAPI server.
5. Listens continuously for completion notifications from the backend.
6. Updates the **Live Feed** automatically when the background worker completes a task.
7. Demonstrates asynchronous processing without requiring the browser page to refresh.

### Example

If the user enters:

```text
Generate PDF Report
```

the frontend sends the request to the API.

The backend places the task in RabbitMQ.

The background consumer processes the task.

When processing is complete, the backend broadcasts the result through WebSocket.

The frontend then automatically displays:

```text
[Processed] Generate PDF Report
```

---

## 🏗️ Full System Architecture

Although this README focuses on the frontend, the frontend depends on the other components of the prototype.

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │      index.html     │
                         │                     │
                         │ HTML + CSS + JS     │
                         └──────────┬──────────┘
                                    │
                         HTTP POST  │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         │       api.py        │
                         └──────────┬──────────┘
                                    │
                           Publish  │
                                    ▼
                         ┌─────────────────────┐
                         │      RabbitMQ       │
                         │ assignment_1_queue  │
                         └──────────┬──────────┘
                                    │
                           Consumer  │
                                    ▼
                         ┌─────────────────────┐
                         │ Background Worker   │
                         │    consumer.py      │
                         └──────────┬──────────┘
                                    │
                              Webhook
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         │ WebSocket Broadcast │
                         └──────────┬──────────┘
                                    │
                         WebSocket  │
                                    ▼
                         ┌─────────────────────┐
                         │      Frontend       │
                         │    Live Feed UI     │
                         └─────────────────────┘
```

---

## 📂 Expected Project Structure

The frontend is normally used alongside the backend and worker scripts:

```text
assignment-1/
│
├── index.html
├── api.py
├── consumer.py
├── README.md
│
└── [optional project files]
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `index.html` | Frontend user interface and WebSocket client |
| `api.py` | FastAPI API gateway and WebSocket broadcaster |
| `consumer.py` | Background RabbitMQ consumer/worker |
| RabbitMQ | Message broker that stores pending tasks |
| `README.md` | Project documentation |

---

## ⚙️ Prerequisites

Before running the frontend, make sure the complete prototype environment is available.

### Required Software

- **Python 3.8 or later**
- **Docker Desktop**
- **Git Bash, PowerShell, Command Prompt, or another terminal**
- A modern web browser such as:
  - Google Chrome
  - Microsoft Edge
  - Mozilla Firefox

### Required Python Packages

Install the backend dependencies with:

```bash
pip install fastapi "uvicorn[standard]" pika requests
```

> **Important:** Install `uvicorn[standard]` rather than only `uvicorn`, because the standard installation provides the WebSocket-related dependencies required by the application.

---

# 🚀 Step-by-Step Setup and Execution

Because the frontend communicates with the FastAPI server and the FastAPI server communicates with RabbitMQ and the background worker, the services must be started in the correct order.

You will normally need **three terminal windows**.

---

## Step 1 — Open the Project Directory

Open your terminal and navigate to the directory containing:

```text
index.html
api.py
consumer.py
```

For example:

```bash
cd path/to/assignment-1
```

Verify that the files are present.

On Git Bash:

```bash
ls
```

On Windows Command Prompt:

```cmd
dir
```

---

## Step 2 — Start RabbitMQ

RabbitMQ acts as the message broker.

Open **Terminal 1** and run:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

Keep this terminal running.

### RabbitMQ Ports

| Port | Purpose |
|---|---|
| `5672` | RabbitMQ application/AMQP connection |
| `15672` | RabbitMQ Management Dashboard |

If RabbitMQ starts successfully, the terminal should show startup information indicating that the broker is running.

### Optional Management Dashboard

The management version of RabbitMQ provides a browser-based dashboard.

Open:

```text
http://localhost:15672
```

If prompted for credentials, the default RabbitMQ development credentials are commonly:

```text
Username: guest
Password: guest
```

Use these only for local development unless your RabbitMQ configuration specifies different credentials.

---

## Step 3 — Start the FastAPI Backend

Open **Terminal 2**.

Navigate to the project directory:

```bash
cd path/to/assignment-1
```

Start the FastAPI application:

```bash
uvicorn api:app --reload
```

The backend should become available at:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

### Why the Backend Is Required

The frontend does not communicate directly with RabbitMQ.

Instead, the browser sends the task to FastAPI:

```text
index.html
    ↓
HTTP POST
    ↓
api.py
    ↓
RabbitMQ
```

The FastAPI server also provides the WebSocket endpoint used by the frontend to receive processing notifications.

---

## Step 4 — Start the Background Consumer

Open **Terminal 3**.

Navigate to the project directory:

```bash
cd path/to/assignment-1
```

Run:

```bash
python consumer.py
```

A successfully running consumer should display a message similar to:

```text
[*] Waiting for messages.
```

Keep this terminal running.

### What the Consumer Does

The consumer:

1. Connects to RabbitMQ.
2. Waits for messages on the queue.
3. Receives tasks published by the FastAPI application.
4. Simulates background processing.
5. Waits approximately 3 seconds.
6. Sends a completion notification back to the API.
7. Allows the API to broadcast the completion event to connected WebSocket clients.

---

# 🌐 Step 5 — Open the Frontend

Locate:

```text
index.html
```

You can open it directly in a modern browser by double-clicking the file.

Alternatively, from the project directory, you may open it through your operating system's file explorer.

The frontend should display the message queue interface.

> **Note:** The frontend depends on the FastAPI server running at `http://127.0.0.1:8000`. Opening `index.html` by itself is not enough to demonstrate the complete application.

---

# 🔌 How the WebSocket Connection Works

When the frontend loads, JavaScript attempts to establish a WebSocket connection with the FastAPI server.

Conceptually:

```text
Browser
   │
   │ WebSocket connection
   ▼
FastAPI
   │
   │ Keeps connection open
   ▼
Browser
```

Unlike a normal HTTP request, the WebSocket connection remains open so that the server can send events to the browser whenever processing is completed.

This is what makes the Live Feed **real-time**.

The browser does not need to repeatedly refresh the page or continuously poll the server.

---

# 🧪 Testing the Frontend

Follow these steps to verify that the complete prototype is working.

## Test 1 — Verify the Frontend Loads

Open `index.html`.

Confirm that:

- The page loads without a browser error.
- The task/message input is visible.
- The **Publish to Queue** button is visible.
- The **Live Feed** section is visible.

---

## Test 2 — Verify the WebSocket Connection

Look at the **Live Feed** section.

The frontend should indicate that it is waiting for processing events, for example:

```text
[System] Waiting for consumer to process messages...
```

The exact wording depends on the implementation in `index.html`.

If the frontend reports a WebSocket connection problem, check that:

1. FastAPI is running.
2. The API is listening on `127.0.0.1:8000`.
3. `uvicorn[standard]` is installed.
4. The WebSocket URL in `index.html` matches the API server.
5. No firewall or browser extension is blocking the connection.

---

## Test 3 — Publish a Message

Enter a test message such as:

```text
Generate PDF Report
```

Click:

```text
Publish to Queue
```

The frontend should immediately provide feedback that the request is being submitted.

The FastAPI server should then publish the message to RabbitMQ.

---

## Test 4 — Observe RabbitMQ Processing

Look at **Terminal 3**, where `consumer.py` is running.

The consumer should receive the message.

For example:

```text
[Received] Generate PDF Report
```

The worker then simulates background processing for approximately three seconds.

---

## Test 5 — Verify Real-Time Completion

After the simulated processing completes, return to the browser.

**Do not refresh the page.**

The Live Feed should automatically display a completion message similar to:

```text
[Processed] Generate PDF Report
```

This confirms that the complete asynchronous workflow is functioning:

```text
User enters message
        ↓
Frontend sends HTTP POST
        ↓
FastAPI receives request
        ↓
FastAPI publishes message
        ↓
RabbitMQ stores message
        ↓
Consumer receives message
        ↓
Consumer processes message
        ↓
Consumer notifies FastAPI
        ↓
FastAPI broadcasts WebSocket event
        ↓
Frontend updates automatically
```

---

# 🧪 Additional Test Messages

Try several different messages to confirm that the system can process multiple tasks.

### Test Message 1

```text
Generate PDF Report
```

### Test Message 2

```text
Send Welcome Email
```

### Test Message 3

```text
Process Customer Order
```

### Test Message 4

```text
Generate Monthly Invoice
```

### Test Message 5

```text
Create Inventory Report
```

Observe whether each completed task appears in the Live Feed.

---

# 🔁 Testing Multiple Messages

You can also test the asynchronous behavior by submitting several messages.

For example:

```text
Task A
Task B
Task C
Task D
```

Submit them through the frontend and observe:

1. The frontend sends each request.
2. RabbitMQ stores pending messages.
3. The consumer processes the messages.
4. Completion notifications are returned through the API.
5. The browser receives the notifications through WebSocket.
6. The Live Feed updates without a page refresh.

This demonstrates the core purpose of a message queue: **decoupling task submission from task processing**.

---

# 🧭 Expected End-to-End Result

A successful test should look approximately like this:

### Browser

```text
[System] WebSocket connected
[Queued] Generate PDF Report
[Processed] Generate PDF Report
```

### FastAPI Terminal

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
...
```

### Consumer Terminal

```text
[*] Waiting for messages.
[Received] Generate PDF Report
[Processed] Generate PDF Report
```

### RabbitMQ

RabbitMQ should have accepted the published message and delivered it to the consumer.

---

# 🛑 Troubleshooting

## Problem 1 — WebSocket Does Not Connect

### Symptoms

The frontend loads, but the Live Feed does not receive real-time updates.

### Possible Causes

- FastAPI is not running.
- Incorrect WebSocket URL.
- `uvicorn[standard]` is not installed.
- The API server is running on a different port.
- Browser/network restrictions are interfering with the connection.

### Solution

Reinstall the dependencies:

```bash
pip install fastapi "uvicorn[standard]" pika requests
```

Then restart FastAPI:

```bash
uvicorn api:app --reload
```

Refresh the frontend.

---

## Problem 2 — `Connection Refused`

### Symptoms

The backend or consumer cannot connect to RabbitMQ.

### Possible Causes

- Docker is not running.
- The RabbitMQ container stopped.
- Port `5672` is already being used.
- RabbitMQ did not start successfully.

### Solution

Check running containers:

```bash
docker ps
```

You should see the `rabbitmq` container.

If it is not running, start it again:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

---

## Problem 3 — RabbitMQ Container Name Already Exists

### Symptoms

Docker reports that a container named `rabbitmq` already exists.

### Solution

Check the containers:

```bash
docker ps -a
```

If an old RabbitMQ container exists, remove it:

```bash
docker rm -f rabbitmq
```

Then start RabbitMQ again:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

---

## Problem 4 — `consumer.py` Cannot Connect

Check the following:

1. RabbitMQ is running.
2. Port `5672` is exposed.
3. The connection settings in `consumer.py` match the RabbitMQ configuration.
4. The required Python packages are installed.
5. The consumer is running from the correct project directory.

Run:

```bash
pip install pika requests
```

Then restart:

```bash
python consumer.py
```

---

## Problem 5 — The Message Is Queued but Never Processed

If the browser reports that the message was successfully queued but nothing appears in the Live Feed:

1. Check Terminal 3.
2. Confirm that `consumer.py` is running.
3. Confirm that the consumer displays:
   ```text
   [*] Waiting for messages.
   ```
4. Check that RabbitMQ is running.
5. Verify that the queue name used by `api.py` matches the queue name used by `consumer.py`.

The queue used by this prototype is:

```text
assignment_1_queue
```

---

## Problem 6 — The Browser Shows a CORS Error

If the browser console reports a CORS-related error, verify that the FastAPI application is configured to permit requests from the origin from which `index.html` is being served.

For local development, check the CORS configuration in:

```text
api.py
```

The exact configuration should match the requirements of your implementation.

---

## Problem 7 — Frontend JavaScript Errors

Open the browser developer tools:

- **Chrome/Edge:** `F12` or `Ctrl + Shift + I`
- **Firefox:** `F12`

Select the **Console** tab.

Look for errors related to:

```text
fetch
WebSocket
CORS
Connection refused
404
500
```

These messages can help identify whether the problem originates from the frontend, API, or WebSocket connection.

---

# 🧹 Stopping the Application

When you finish testing:

### Stop FastAPI

In Terminal 2, press:

```text
Ctrl + C
```

### Stop the Consumer

In Terminal 3, press:

```text
Ctrl + C
```

### Stop RabbitMQ

In Terminal 1, press:

```text
Ctrl + C
```

Because the Docker command uses:

```text
--rm
```

the RabbitMQ container is automatically removed when it stops.

---

# 🔐 Development Notes

This prototype is designed for **local development and reconnaissance/learning purposes**.

The implementation demonstrates:

- Asynchronous task processing
- Producer-consumer architecture
- RabbitMQ message queues
- FastAPI REST endpoints
- WebSocket communication
- Background workers
- Real-time browser updates
- Separation of frontend and backend responsibilities

It is not intended to be treated as a production-ready messaging platform without additional security, monitoring, persistence, error handling, authentication, and deployment configuration.

---

# 🎯 Learning Objectives

This frontend demonstrates several important software engineering concepts.

## 1. Asynchronous Communication

The browser does not wait for the background worker to finish processing before continuing.

Instead:

```text
Submit → Queue → Continue
```

The completion event arrives later.

---

## 2. Message Queues

RabbitMQ temporarily holds tasks so that producers and consumers do not need to operate at exactly the same time.

```text
Producer → Queue → Consumer
```

---

## 3. Decoupling

The frontend does not need to know how the worker performs the task.

The frontend only needs to know:

```text
Submit task
Receive completion event
```

The backend and worker handle the processing details.

---

## 4. WebSockets

WebSockets allow the server to push information to the browser immediately.

This is different from repeatedly polling the server for updates.

```text
HTTP:
Browser → Server
Browser → Server
Browser → Server

WebSocket:
Browser ←→ Server
          ↓
       Event
          ↓
       Browser
```

---

## 5. Real-Time User Experience

Because the frontend receives completion events automatically, the user does not have to:

- Refresh the browser.
- Submit the same request repeatedly.
- Manually check whether the task has finished.

---

# 📋 Quick Start Summary

For experienced users, the complete setup can be summarized as:

### Terminal 1 — RabbitMQ

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

### Terminal 2 — FastAPI

```bash
pip install fastapi "uvicorn[standard]" pika requests
uvicorn api:app --reload
```

### Terminal 3 — Consumer

```bash
python consumer.py
```

### Browser

Open:

```text
index.html
```

Then enter a message and click:

```text
Publish to Queue
```

Expected result:

```text
Message
   ↓
RabbitMQ
   ↓
Consumer
   ↓
Processing
   ↓
FastAPI
   ↓
WebSocket
   ↓
Live Feed
```

---

# 👨‍💻 Author

**Emmanuel Chijinkem Ukah**

**Project:** Real-Time Message Queue Prototype — Assignment 1  
**Program:** Power Learn Project  
**Phase:** Solo Reconnaissance Phase

---

# 📄 License

This project is an educational prototype developed for the Power Learn Project assignment and is intended for learning, demonstration, and reconnaissance purposes.
