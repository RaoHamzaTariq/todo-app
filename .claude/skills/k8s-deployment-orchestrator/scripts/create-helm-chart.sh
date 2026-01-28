#!/bin/bash
# create-helm-chart.sh
# Script to create a basic Helm chart structure for a microservice

set -e

CHART_NAME="$1"
SERVICE_TYPE="$2"  # frontend, backend, mcp-server

if [ -z "$CHART_NAME" ] || [ -z "$SERVICE_TYPE" ]; then
    echo "Usage: $0 <chart-name> <service-type>"
    echo "Service type must be one of: frontend, backend, mcp-server"
    exit 1
fi

if [ "$SERVICE_TYPE" != "frontend" ] && [ "$SERVICE_TYPE" != "backend" ] && [ "$SERVICE_TYPE" != "mcp-server" ]; then
    echo "Error: Service type must be one of: frontend, backend, mcp-server"
    exit 1
fi

echo "Creating Helm chart: $CHART_NAME for $SERVICE_TYPE service..."

# Create chart directory structure
mkdir -p "$CHART_NAME"/{templates,charts}

# Create Chart.yaml
cat > "$CHART_NAME/Chart.yaml" << EOF
apiVersion: v2
name: $CHART_NAME
description: A Helm chart for $SERVICE_TYPE service
type: application
version: 0.1.0
appVersion: "1.0.0"
EOF

# Create values.yaml with service-specific defaults
cat > "$CHART_NAME/values.yaml" << EOF
# Default values for $CHART_NAME
replicaCount: 1

image:
  repository: my-registry/${CHART_NAME}
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

resources:
  # Recommended values for $SERVICE_TYPE - adjust as needed
EOF

case $SERVICE_TYPE in
    "frontend")
        cat >> "$CHART_NAME/values.yaml" << EOF
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi
EOF
        ;;
    "backend")
        cat >> "$CHART_NAME/values.yaml" << EOF
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
EOF
        ;;
    "mcp-server")
        cat >> "$CHART_NAME/values.yaml" << EOF
  limits:
    cpu: 300m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi
EOF
        ;;
esac

cat >> "$CHART_NAME/values.yaml" << EOF

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
EOF

# Create basic deployment template
cat > "$CHART_NAME/templates/deployment.yaml" << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "{{ .Chart.Name }}" . }}
  labels:
    {{- include "{{ .Chart.Name }}.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "{{ .Chart.Name }}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "{{ .Chart.Name }}.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "{{ .Chart.Name }}.serviceAccountName" . }}
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
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- with .Values.env }}
          env:
            {{- range $key, $value := . }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
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
EOF

# Create service template
cat > "$CHART_NAME/templates/service.yaml" << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "{{ .Chart.Name }}.fullname" . }}
  labels:
    {{- include "{{ .Chart.Name }}.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "{{ .Chart.Name }}.selectorLabels" . | nindent 4 }}
EOF

# Create helper templates
cat > "$CHART_NAME/templates/_helpers.tpl" << 'EOF'
{{/*
Expand the name of the chart.
*/}}
{{- define "{{ .Chart.Name }}.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "{{ .Chart.Name }}.fullname" -}}
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
{{- define "{{ .Chart.Name }}.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{ include "{{ .Chart.Name }}.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "{{ .Chart.Name }}.selectorLabels" -}}
app.kubernetes.io/name: {{ include "{{ .Chart.Name }}.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "{{ .Chart.Name }}.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "{{ .Chart.Name }}.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
EOF

echo "Helm chart '$CHART_NAME' for $SERVICE_TYPE service created successfully!"
echo "Directory structure:"
tree "$CHART_NAME" 2>/dev/null || find "$CHART_NAME" -type f | sort