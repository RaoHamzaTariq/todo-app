# Kubernetes Best Practices Reference

## Resource Management

### CPU and Memory Requests/Limits Guidelines

#### Frontend Services (Next.js, React, etc.)
- **CPU Request**: 50-100m (minimum 50m)
- **CPU Limit**: 200-500m
- **Memory Request**: 64-128Mi
- **Memory Limit**: 256-512Mi

#### Backend Services (FastAPI, Express, etc.)
- **CPU Request**: 100-200m (minimum 50m)
- **CPU Limit**: 300-800m
- **Memory Request**: 128-256Mi
- **Memory Limit**: 512-1024Mi

#### MCP Servers and API Gateways
- **CPU Request**: 50-100m
- **CPU Limit**: 100-300m
- **Memory Request**: 64-128Mi
- **Memory Limit**: 128-256Mi

### Horizontal Pod Autoscaler (HPA) Configuration
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{service-name}}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{deployment-name}}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Health Checks

### Liveness Probes
- Use for crash detection, not as a restart mechanism
- Should be more tolerant than readiness probes
- Generally higher timeout values
- Path should check actual service functionality

### Readiness Probes
- Use to determine if pod is ready to serve traffic
- Should be more conservative than liveness probes
- Check dependencies (DB, cache, etc.) if needed
- Lower timeout values than liveness

### Common Health Check Endpoints
- `/health` or `/healthz` for liveness
- `/ready` or `/readyz` for readiness
- `/metrics` for Prometheus metrics

## Security Best Practices

### Pod Security Standards
```yaml
# Example securityContext for deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: {{container-name}}
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

### Secret Management
- Store sensitive data in Kubernetes Secrets, not ConfigMaps
- Use sealed-secrets or similar for encrypted secrets in Git
- Mount secrets as volumes instead of environment variables when possible
- Use external secrets managers for production (HashiCorp Vault, AWS Secrets Manager)

## Networking

### Service Types
- **ClusterIP**: Default, only accessible within cluster
- **NodePort**: Accessible via `<NodeIP>:<NodePort>` (30000-32767)
- **LoadBalancer**: Exposes service externally using cloud provider's LB
- **ExternalName**: Maps service to external DNS name

### Ingress Configuration
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{app-name}}-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: {{hostname}}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80
```

## Monitoring and Logging

### Prometheus Metrics Endpoint
```yaml
# Add to container spec
ports:
- name: metrics
  containerPort: 9090
  protocol: TCP
```

### Structured Logging
- Use JSON format for application logs
- Include structured fields (level, timestamp, service, trace-id)
- Consider using fluentd or similar for log aggregation

## Common Helm Template Functions

### Helper Templates (_helpers.tpl)
```go
{{/*
Expand the name of the chart.
*/}}
{{- define "{{.Chart.Name}}.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "{{.Chart.Name}}.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "{{.Chart.Name}}.labels" -}}
helm.sh/chart: {{ include "{{.Chart.Name}}.chart" . }}
{{ include "{{.Chart.Name}}.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```