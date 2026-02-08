# Kafka Producer Configuration Template

# This template can be used to configure Kafka producers in your application

producer_config = {
    # Bootstrap servers - update based on your environment
    'bootstrap.servers': 'kafka:9092',  # For local Minikube
    # 'bootstrap.servers': 'your-oracle-oke-kafka-service:9092',  # For Oracle OKE

    # Client configuration
    'client.id': 'todo-chatbot-producer',

    # Serialization
    'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
    'value.serializer': 'org.apache.kafka.common.serialization.StringSerializer',

    # Delivery settings
    'acks': 'all',  # Wait for all replicas to acknowledge
    'retries': 3,
    'batch.size': 16384,
    'linger.ms': 5,
    'buffer.memory': 33554432,

    # Compression
    'compression.type': 'snappy',  # Good balance of speed/compression

    # Security (if needed)
    # 'security.protocol': 'SASL_SSL',
    # 'sasl.mechanism': 'PLAIN',
    # 'sasl.username': 'your_username',
    # 'sasl.password': 'your_password',
}

# Example usage in Python with confluent-kafka
"""
from confluent_kafka import Producer
import json

def create_kafka_producer():
    return Producer(producer_config)

def publish_task_event(producer, topic, event_data):
    # Convert event data to JSON string
    event_json = json.dumps(event_data)

    # Produce the message
    producer.produce(
        topic=topic,
        key=event_data['user_id'],  # Use user_id as partition key for consistent routing
        value=event_json,
        callback=delivery_callback
    )

    # Wait for any outstanding messages to be delivered
    producer.flush()

def delivery_callback(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
"""