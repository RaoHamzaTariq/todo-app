
import sys
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

sys.path.append("/app")

from event_services.recurring_task_service.src.kafka_consumer import KafkaConsumerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recurring-task-service")

consumer_service = KafkaConsumerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Recurring Task Service...")
    await consumer_service.initialize()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "recurring-task-events",
            "route": "/events/recurring-task-created",
            "metadata": {"rawPayload": "true"}
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-updated",
            "metadata": {"rawPayload": "true"}
        }
    ]

@app.post("/events/recurring-task-created")
async def handle_recurring_task_created(request: Request):
    try:
        data = await request.json()
        await consumer_service.handle_recurring_task_created_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling recurring-task-created: {e}")
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
