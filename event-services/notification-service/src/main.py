
import sys
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

sys.path.append("/app")

# Import NotificationSender
# It requires DaprClient and AIOKafkaProducer
# But if we use Dapr PubSub Binding (Push), we might not need KafkaProducer directly?
# NotificationSender sends "notification-events" (notification sent).
# It uses Kafka Producer for that.
# Ideally it should use Dapr Binding or PubSub to publish.
# But let's stick to what it has, but initialize correctly.
# It expects AIOKafkaProducer.
# We should probably refactor it to usage Dapr Client PublishEvent if possible.
# But to change minimal code, let's keep it or mock it.
# Check notification_sender.py: it uses kafka_producer.send_and_wait.
# We will initialize it with a real or mock producer.
# Since we have Dapr, we can use Dapr Client to publish to 'notification-events' topic.
# Let's subclass or monkeypatch if we want Dapr.
# Or just use aiokafka if KAFKA_BROKER is set.

from event_services.notification_service.src.notification_sender import NotificationSender
from dapr.clients import DaprClient
import aiokafka

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-service")

notification_sender = None
dapr_client = None
kafka_producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global notification_sender, dapr_client, kafka_producer
    logger.info("Starting Notification Service...")
    
    dapr_client = DaprClient()
    
    # Initialize Kafka Producer
    # Get broker from env
    kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    logger.info(f"Connecting to Kafka at {kafka_broker}")
    
    kafka_producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=kafka_broker,
        value_serializer=lambda x: x # It encodes manually in _publish_notification_sent_event
    )
    await kafka_producer.start()
    
    notification_sender = NotificationSender(dapr_client, kafka_producer)
    
    yield
    
    await kafka_producer.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminder-events", # reminder.triggered
            "route": "/events/reminder-triggered",
            "metadata": {"rawPayload": "true"}
        }
    ]

@app.post("/events/reminder-triggered")
async def handle_reminder_triggered(request: Request):
    try:
        data = await request.json()
        # Expecting reminder_data
        if "data" in data and "type" in data:
             # CloudEvent
             payload = data["data"]
        else:
             payload = data
             
        # Process
        await notification_sender.process_reminder_event(payload)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling reminder-triggered: {e}")
        return {"status": "error"}

@app.get("/health")
def health():
    return {"status": "healthy"}
