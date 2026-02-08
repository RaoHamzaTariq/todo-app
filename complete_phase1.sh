#!/bin/bash
# Phase 1 Completion Script - Run when adequate resources are available

echo "Completing Phase 1: Environment & Cluster Setup"

# Wait for Dapr operator to be ready
echo "Waiting for Dapr operator to be ready..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy Kafka cluster
echo "Deploying Kafka cluster..."
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 5Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 2Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Wait for Kafka cluster to be ready
echo "Waiting for Kafka cluster to be ready..."
kubectl wait --for=condition=Ready kafka/my-cluster -n kafka --timeout=300s

# Apply Dapr components
echo "Applying Dapr components..."
kubectl apply -f kafka-dapr-component.yaml
kubectl apply -f postgresql-dapr-component.yaml

# Verify all components
echo "Verifying installations..."
echo "Dapr status:"
dapr status -k
echo "Kafka pods:"
kubectl get pods -n kafka
echo "Database pods:"
kubectl get pods
echo "All services:"
kubectl get svc

echo "Phase 1 setup completed!"