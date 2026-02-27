FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend for imports
COPY backend/ /app/backend/

# Copy event services (renaming to event_services for import)
COPY event-services/ /app/event_services/

# Rename directories to use underscores instead of hyphens for Python imports
RUN mv /app/event_services/reminder-service /app/event_services/reminder_service && \
    mv /app/event_services/recurring-task-service /app/event_services/recurring_task_service && \
    mv /app/event_services/audit-log-service /app/event_services/audit_log_service && \
    mv /app/event_services/notification-service /app/event_services/notification_service

# Ensure init files exist (simple touch)
RUN touch /app/event_services/__init__.py && \
    touch /app/event_services/reminder_service/__init__.py && \
    touch /app/event_services/reminder_service/src/__init__.py


EXPOSE 80

CMD ["uvicorn", "event_services.reminder_service.src.main:app", "--host", "0.0.0.0", "--port", "80"]
