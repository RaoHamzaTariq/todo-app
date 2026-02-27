
import sys
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

sys.path.append("/app")

from event_services.audit_log_service.src.kafka_consumer import KafkaConsumerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit-log-service")

# Configure log path
log_file = "/app/logs/audit.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

consumer_service = KafkaConsumerService(log_file_path=log_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Audit Log Service...")
    await consumer_service.initialize()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/audit/task",
            "metadata": {"rawPayload": "true"}
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminder-events",
            "route": "/events/audit/reminder",
            "metadata": {"rawPayload": "true"}
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "recurring-task-events",
            "route": "/events/audit/recurring",
            "metadata": {"rawPayload": "true"}
        }
    ]

# Handler logic requires dispatching based on event type
# KafkaConsumerService has specific handlers but Dapr calls one endpoint per topic usually?
# Or we can route all to one.
# Let's map routes.

@app.post("/events/audit/task")
async def handle_audit_task(request: Request):
    try:
        data = await request.json()
        event_type = data.get("event_type")
        if event_type == "task.created":
            await consumer_service.handle_task_created_event(data)
        elif event_type == "task.updated":
            await consumer_service.handle_task_updated_event(data)
        else:
             await consumer_service.handle_generic_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling audit task event: {e}")
        return {"status": "error"}

@app.post("/events/audit/reminder")
async def handle_audit_reminder(request: Request):
    try:
        data = await request.json()
        event_type = data.get("event_type")
        if event_type == "reminder.scheduled":
             await consumer_service.handle_reminder_scheduled_event(data)
        else:
             await consumer_service.handle_generic_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling audit reminder event: {e}")
        return {"status": "error"}

@app.post("/events/audit/recurring")
async def handle_audit_recurring(request: Request):
    try:
        data = await request.json()
        if data.get("event_type") == "recurring-task.created":
             await consumer_service.handle_recurring_task_created_event(data)
        else:
             await consumer_service.handle_generic_event(data)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling audit recurring event: {e}")
        return {"status": "error"}

@app.get("/health")
def health():
    return {"status": "healthy"}
