# Event Architecture Skill

This skill provides guidance and tools for managing the event-driven system for the Todo Chatbot using Kafka and Dapr.

## Purpose
Manage event-driven system for Todo Chatbot, including:
- Designing Kafka topics, consumers, and producers
- Ensuring event flow covers reminders, recurring tasks, audit logs, and real-time sync
- Validating event schemas and Dapr Pub/Sub integration
- Ensuring cluster compatibility

## Key Features
- Kafka topic design and management
- Dapr integration for pub/sub
- Event schema validation
- Consumer and producer implementation guidance
- Cluster compatibility assurance

## Files Included
- `SKILL.md` - Main skill documentation
- `references/kafka-dapr-config.md` - Detailed configuration examples
- `scripts/validate_event_schema.py` - Event schema validation tool
- `assets/kafka-producer-config-template.py` - Configuration template

## Usage
Use this skill when implementing or managing event-driven architecture components for the Todo Chatbot, particularly for Kafka and Dapr integration.