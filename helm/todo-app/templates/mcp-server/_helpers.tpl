{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.mcp-server.name" -}}
{{- default .Chart.Name .Values.mcpServer.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-app.mcp-server.fullname" -}}
{{- if .Values.mcpServer.fullnameOverride }}
{{- .Values.mcpServer.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.mcpServer.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.mcp-server.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.mcp-server.labels" -}}
helm.sh/chart: {{ include "todo-app.mcp-server.chart" . }}
{{ include "todo-app.mcp-server.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.mcp-server.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.mcp-server.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}