
import sys
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

# Ensure backend and event-services are in path
# Assuming Dockerfile copies them to /app/backend and /app/event_services
sys.path.append("/app")

# Import services
from event_services.reminder_service.src.kafka_consumer import KafkaConsumerService
# from event_services.reminder_service.src.reminder_processor import get_reminder_processor
# from backend.src.services.reminder_service import ReminderService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reminder-service")

consumer_service = KafkaConsumerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Reminder Service...")
    await consumer_service.initialize()
    # Processor initialization would go here if we can manage DB session correctly
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminder-events",
            "route": "/events/reminder-scheduled",
            "metadata": {"rawPayload": "true"}
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-created",
            "metadata": {"rawPayload": "true"}
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-updated",
            "metadata": {"rawPayload": "true"}
        }
    ]

@app.post("/events/reminder-scheduled")
async def handle_reminder_scheduled(request: Request):
    try:
        data = await request.json()
        await consumer_service.handle_reminder_scheduled_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling reminder-scheduled: {e}")
        return {"status": "error"}

@app.post("/events/task-created")
async def handle_task_created(request: Request):
    try:
        data = await request.json()
        await consumer_service.handle_task_created_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling task-created: {e}")
        return {"status": "error"}

@app.post("/events/task-updated")
async def handle_task_updated(request: Request):
    try:
        data = await request.json()
        await consumer_service.handle_task_updated_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling task-updated: {e}")
        return {"status": "error"}

@app.get("/health")
def health():
    return {"status": "healthy"}
