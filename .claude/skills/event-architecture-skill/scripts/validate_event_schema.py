#!/usr/bin/env python3
"""
Event Schema Validator Script

This script validates event schemas against predefined JSON schemas
for the Todo Chatbot event-driven architecture.
"""

import json
import sys
from jsonschema import validate, ValidationError
from datetime import datetime

# Define schemas for different event types
SCHEMAS = {
    "task-events": {
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
        "additionalProperties": False
    },
    "reminders": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "reminder_id": {
                "type": "string",
                "minLength": 1
            },
            "user_id": {
                "type": "string",
                "minLength": 1
            },
            "task_id": {
                "type": "integer",
                "minimum": 1
            },
            "scheduled_time": {
                "type": "string",
                "format": "date-time"
            },
            "sent_time": {
                "type": ["string", "null"],
                "format": "date-time"
            },
            "status": {
                "type": "string",
                "enum": ["pending", "sent", "failed"]
            }
        },
        "required": ["reminder_id", "user_id", "task_id", "scheduled_time", "status"],
        "additionalProperties": False
    },
    "task-updates": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "minLength": 1
            },
            "task_id": {
                "type": "integer",
                "minimum": 1
            },
            "action": {
                "type": "string",
                "enum": ["updated_title", "updated_description", "changed_status", "changed_due_date"]
            },
            "old_value": {
                "type": "object"
            },
            "new_value": {
                "type": "object"
            },
            "timestamp": {
                "type": "string",
                "format": "date-time"
            },
            "source": {
                "type": "string",
                "enum": ["api", "mcp_tool", "recurring_task"]
            }
        },
        "required": ["user_id", "task_id", "action", "timestamp", "source"],
        "additionalProperties": False
    },
    "audit-logs": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "minLength": 1
            },
            "event_type": {
                "type": "string",
                "enum": ["login", "logout", "task_access", "data_export", "security_event"]
            },
            "timestamp": {
                "type": "string",
                "format": "date-time"
            },
            "source_ip": {
                "type": "string"
            },
            "user_agent": {
                "type": "string"
            },
            "details": {
                "type": "object"
            }
        },
        "required": ["user_id", "event_type", "timestamp"],
        "additionalProperties": False
    }
}


def validate_event_schema(topic, event_data):
    """
    Validate an event against the schema for its topic

    Args:
        topic (str): The Kafka topic name
        event_data (dict): The event data to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if topic not in SCHEMAS:
        return False, f"Unknown topic: {topic}. Available topics: {list(SCHEMAS.keys())}"

    schema = SCHEMAS[topic]

    try:
        validate(instance=event_data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, f"Schema validation error: {e.message}"


def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_event_schema.py <topic_name> '<event_json>'")
        print("Example: python validate_event_schema.py task-events '{\"event_type\":\"task_created\",\"user_id\":\"user123\",\"task_id\":1,\"timestamp\":\"2023-01-01T00:00:00Z\",\"data\":{}}'")
        sys.exit(1)

    topic = sys.argv[1]
    event_str = sys.argv[2]

    try:
        event_data = json.loads(event_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    is_valid, error_msg = validate_event_schema(topic, event_data)

    if is_valid:
        print("✓ Event is valid")
        sys.exit(0)
    else:
        print(f"✗ Event validation failed: {error_msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()