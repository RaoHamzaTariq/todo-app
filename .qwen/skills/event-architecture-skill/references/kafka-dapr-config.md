# Kafka and Dapr Configuration Reference

## Kafka Topics for Todo Chatbot

### Topic Definitions

#### task-events
- **Purpose**: All task lifecycle events (create, update, delete, complete)
- **Partitions**: 3 (adjust based on throughput)
- **Replication Factor**: 3
- **Retention**: 7 days
- **Key**: user_id
- **Value Schema**:
```json
{
  "event_type": "task_created|task_updated|task_deleted|task_completed",
  "user_id": "string",
  "task_id": "int",
  "timestamp": "ISO8601",
  "data": {
    // task-specific data
  }
}
```

#### reminders
- **Purpose**: Scheduled reminder events
- **Partitions**: 2
- **Replication Factor**: 3
- **Retention**: 1 day (short-lived events)
- **Key**: task_id
- **Value Schema**:
```json
{
  "reminder_id": "string",
  "user_id": "string",
  "task_id": "int",
  "scheduled_time": "ISO8601",
  "sent_time": "ISO8601|null",
  "status": "pending|sent|failed"
}
```

#### task-updates
- **Purpose**: Task modification events for audit and sync
- **Partitions**: 3
- **Replication Factor**: 3
- **Retention**: 30 days (longer for audit)
- **Key**: user_id
- **Value Schema**:
```json
{
  "user_id": "string",
  "task_id": "int",
  "action": "updated_title|updated_description|changed_status|changed_due_date",
  "old_value": {},
  "new_value": {},
  "timestamp": "ISO8601",
  "source": "api|mcp_tool|recurring_task"
}
```

#### audit-logs
- **Purpose**: System audit events
- **Partitions**: 2
- **Replication Factor**: 3
- **Retention**: 90 days (compliance requirement)
- **Key**: user_id
- **Value Schema**:
```json
{
  "user_id": "string",
  "event_type": "login|logout|task_access|data_export|security_event",
  "timestamp": "ISO8601",
  "source_ip": "string",
  "user_agent": "string",
  "details": {}
}
```

## Dapr Component Configuration

### Kafka Pub/Sub Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: clientID
    value: "dapr-kafka-client"
  - name: maxMessageBytes
    value: "1048576"
  - name: consumeRetryInterval
    value: "200ms"
  - name: disableTls
    value: "true"
  - name: version
    value: "1.0.0"
```

### State Store Component (for transient state)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-master:6379"
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

## Dapr Service Invocation Examples

### Publishing an Event
```python
import dapr.clients
from dapr.clients import DaprClient

def publish_task_event(user_id, task_id, event_type, data):
    with DaprClient() as client:
        # Publish an event to the task-events topic
        client.publish_event(
            pubsub_name='kafka-pubsub',
            topic_name='task-events',
            data=json.dumps({
                "event_type": event_type,
                "user_id": user_id,
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }),
            metadata={
                "partitionKey": user_id
            }
        )
```

### Subscribing to Events
```python
from dapr.ext.grpc import App
import json

app = App()

@app.subscribe(pubsub_name='kafka-pubsub', topic='task-events')
def handle_task_events(event_data):
    # Parse the event
    event = json.loads(event_data.data())

    # Validate user permissions
    if not validate_user_permissions(event['user_id']):
        return

    # Process the event based on type
    if event['event_type'] == 'task_created':
        handle_task_created(event)
    elif event['event_type'] == 'task_updated':
        handle_task_updated(event)
    # ... other event types
```

## Event Schema Validation

### JSON Schema for Task Events
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "event_type": {
      "type": "string",
      "enum": ["task_created", "task_updated", "task_deleted", "task_completed"]
    },
    "user_id": {
      "type": "string",
      "minLength": 1
    },
    "task_id": {
      "type": "integer",
      "minimum": 1
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "data": {
      "type": "object"
    }
  },
  "required": ["event_type", "user_id", "task_id", "timestamp"],
  "additionalProperties": false
}
```

## Consumer Group Configuration

### Consumer Group Settings
```yaml
# Consumer-specific configurations
consumer_configs:
  reminder-processor:
    group_id: "reminder-service-group"
    topic: "reminders"
    num_consumers: 2
    max_poll_records: 100
    session_timeout_ms: 30000

  audit-logger:
    group_id: "audit-service-group"
    topic: "audit-logs"
    num_consumers: 1  # Sequential processing required
    max_poll_records: 50
    session_timeout_ms: 45000

  task-sync:
    group_id: "sync-service-group"
    topic: "task-updates"
    num_consumers: 3
    max_poll_records: 200
    session_timeout_ms: 30000
```

## Error Handling Patterns

### Dead Letter Queue Configuration
```python
def process_event_with_dlq(topic, event):
    try:
        # Process the event
        result = process_event(event)
        return result
    except ValidationError as e:
        # Send to dead letter queue for invalid events
        send_to_dlq("dlq-invalid-events", {
            "original_topic": topic,
            "event": event,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
        return False
    except Exception as e:
        # Send to DLQ for processing errors (with retry limits)
        current_retry_count = event.get('retry_count', 0)
        if current_retry_count < MAX_RETRY_COUNT:
            # Requeue with incremented retry count
            event['retry_count'] = current_retry_count + 1
            send_to_topic(topic, event)  # Will retry
        else:
            # Move to DLQ after max retries
            send_to_dlq("dlq-processing-errors", {
                "original_topic": topic,
                "event": event,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        return False
```

## Monitoring and Observability

### Kafka Metrics to Monitor
- Consumer lag per topic and partition
- Message production rate
- Message consumption rate
- Error rates in consumer applications
- Broker availability and performance

### Dapr Observability Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: zipkin
spec:
  type: exporters.zipkin
  version: v1
  metadata:
  - name: enabled
    value: "true"
  - name: exporterType
    value: "zipkin"
  - name: endpointAddress
    value: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
```