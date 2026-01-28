---
name: k8s-deployment-orchestrator
description: Generate Kubernetes deployment specifications for microservices including Frontend (Next.js), Backend (FastAPI + JWT + OpenAI Agents SDK), and MCP Server with best practices for resource management, probes, and configuration. Use when deploying applications to Kubernetes clusters, creating Helm charts, or configuring containerized services with proper resource limits, health checks, and environment configurations.
---

# Kubernetes Deployment Orchestrator

## Overview

This skill teaches Claude how to generate Kubernetes deployment specifications for microservices including Frontend (Next.js), Backend (FastAPI + JWT + OpenAI Agents SDK), and MCP Server. It covers best practices for resource management, health checks, and configuration management.

## When to Use This Skill

Use this skill when:
- Deploying applications to Kubernetes clusters
- Creating Helm charts for microservices
- Configuring containerized services with proper resource limits
- Setting up health checks (readiness/liveness probes)
- Managing environment configurations for different environments
- Generating Kubernetes manifests with security best practices

## Prerequisites

Before using this skill, ensure you have:
- Access to the project's codebase to understand service dependencies
- Knowledge of the services that need to be deployed
- Understanding of resource requirements for each service

## Step-by-Step Instructions

### Step 1: Analyze the Service Architecture

1. Examine the project structure to identify all services that need to be deployed
2. Determine service dependencies and communication patterns
3. Identify required environment variables and secrets
4. Assess resource requirements for each service

### Step 2: Create Base Kubernetes Manifests

For each service, create the following Kubernetes resources:

#### Deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{service-name}}
  labels:
    app: {{service-name}}
spec:
  replicas: {{replica-count}}
  selector:
    matchLabels:
      app: {{service-name}}
  template:
    metadata:
      labels:
        app: {{service-name}}
    spec:
      containers:
      - name: {{service-name}}
        image: {{image-repository}}:{{image-tag}}
        ports:
        - containerPort: {{port}}
        env:
        - name: ENV_VAR_NAME
          valueFrom:
            secretKeyRef:
              name: {{secret-name}}
              key: {{key-name}}
        resources:
          requests:
            memory: "{{memory-request}}"
            cpu: "{{cpu-request}}"
          limits:
            memory: "{{memory-limit}}"
            cpu: "{{cpu-limit}}"
        livenessProbe:
          httpGet:
            path: /health
            port: {{port}}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: {{port}}
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{service-name}}
  labels:
    app: {{service-name}}
spec:
  selector:
    app: {{service-name}}
  ports:
    - protocol: TCP
      port: {{service-port}}
      targetPort: {{container-port}}
  type: ClusterIP  # Use NodePort for external access if needed
```

### Step 3: Configure Environment Variables and Secrets

1. Create Secret manifests for sensitive information:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{service-name}}-secrets
type: Opaque
data:
  # Base64 encoded values
  JWT_SECRET: <base64-encoded-value>
  DATABASE_URL: <base64-encoded-value>
```

2. Create ConfigMap for non-sensitive configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{service-name}}-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
```

### Step 4: Create Helm Chart Structure

Organize manifests into a Helm chart structure:
```
chart-name/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── _helpers.tpl
│   ├── secrets.yaml
│   └── configmap.yaml
└── charts/
```

### Step 5: Define Values.yaml with Best Practices

```yaml
# Default values for the chart
replicaCount: 1

image:
  repository: my-registry/{{service-name}}
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion
  tag: ""

service:
  type: ClusterIP
  port: 80

resources:
  # Recommended values for production
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

nodeSelector: {}

tolerations: []

affinity: {}
```

### Step 6: Template Kubernetes Manifests with Helm

In `templates/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "{{project-name}}.fullname" . }}
  labels:
    {{- include "{{project-name}}.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "{{project-name}}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "{{project-name}}.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "{{project-name}}.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- with .Values.volumeMounts }}
          volumeMounts:
            {{- toYaml . | nindent 12 }}
          {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## Service-Specific Configurations

### Frontend (Next.js) Deployment

For Next.js applications, consider these specific configurations:

```yaml
# resources.limits for frontend
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi

# Additional environment variables
env:
- name: NEXT_PUBLIC_API_URL
  value: "http://backend-service:8000"
```

### Backend (FastAPI) Deployment

For FastAPI applications, use these configurations:

```yaml
# resources.limits for backend
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

# Environment variables for FastAPI
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: url
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: jwt-secret
      key: secret
```

### MCP Server Deployment

For MCP servers, consider these configurations:

```yaml
# resources.limits for MCP server
resources:
  limits:
    cpu: 300m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi

# MCP-specific environment variables
env:
- name: MCP_PORT
  value: "3000"
- name: MCP_CONFIG_PATH
  value: "/etc/mcp/config.yaml"
```

## Best Practices

### Resource Management
- Set realistic CPU and memory requests/limits based on actual usage
- Use Vertical Pod Autoscaler (VPA) for optimization in development
- Monitor resource usage and adjust accordingly

### Health Checks
- Implement meaningful readiness probes that check actual service readiness
- Use liveness probes for crash detection, not as a restart mechanism
- Set appropriate timeouts and thresholds

### Security
- Run containers as non-root users
- Use secrets for sensitive data, not configmaps
- Implement network policies for service-to-service communication
- Enable RBAC where appropriate

### Observability
- Include proper logging configuration
- Expose metrics endpoints
- Use structured logging for easier analysis

## Common Validation Steps

1. Verify all referenced secrets and configmaps exist
2. Check that service ports match container ports
3. Validate image pull secrets if using private registries
4. Confirm resource requests/limits are appropriate for the target environment
5. Ensure health check endpoints are correctly configured

## Troubleshooting

Common issues and solutions:

- **Pod stuck in Pending**: Check resource requests exceed cluster capacity
- **CrashLoopBackOff**: Verify environment variables and dependencies are correctly configured
- **ImagePullBackOff**: Confirm image repository and tag are correct and accessible
- **Liveness probe failed**: Increase timeout values or check if the application is healthy

## Example Complete Deployment

See `examples/` directory for complete deployment examples for different service types.