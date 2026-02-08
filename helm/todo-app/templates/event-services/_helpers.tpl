{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.event-services.name" -}}
{{- default .Chart.Name .Values.eventServices.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-app.event-services.fullname" -}}
{{- if .Values.eventServices.fullnameOverride }}
{{- .Values.eventServices.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.eventServices.nameOverride }}
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
{{- define "todo-app.event-services.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.event-services.labels" -}}
helm.sh/chart: {{ include "todo-app.event-services.chart" . }}
{{ include "todo-app.event-services.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.event-services.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.event-services.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Reminder Service helpers
*/}}
{{- define "todo-app.reminder-service.name" -}}
{{- default (printf "%s-reminder-service" .Chart.Name) .Values.eventServices.reminderService.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-app.reminder-service.fullname" -}}
{{- if .Values.eventServices.reminderService.fullnameOverride }}
{{- .Values.eventServices.reminderService.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-reminder-service" .Chart.Name) .Values.eventServices.reminderService.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Recurring Task Service helpers
*/}}
{{- define "todo-app.recurring-task-service.name" -}}
{{- default (printf "%s-recurring-task-service" .Chart.Name) .Values.eventServices.recurringTaskService.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-app.recurring-task-service.fullname" -}}
{{- if .Values.eventServices.recurringTaskService.fullnameOverride }}
{{- .Values.eventServices.recurringTaskService.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-recurring-task-service" .Chart.Name) .Values.eventServices.recurringTaskService.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Audit Log Service helpers
*/}}
{{- define "todo-app.audit-log-service.name" -}}
{{- default (printf "%s-audit-log-service" .Chart.Name) .Values.eventServices.auditLogService.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-app.audit-log-service.fullname" -}}
{{- if .Values.eventServices.auditLogService.fullnameOverride }}
{{- .Values.eventServices.auditLogService.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-audit-log-service" .Chart.Name) .Values.eventServices.auditLogService.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Notification Service helpers
*/}}
{{- define "todo-app.notification-service.name" -}}
{{- default (printf "%s-notification-service" .Chart.Name) .Values.eventServices.notificationService.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-app.notification-service.fullname" -}}
{{- if .Values.eventServices.notificationService.fullnameOverride }}
{{- .Values.eventServices.notificationService.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (printf "%s-notification-service" .Chart.Name) .Values.eventServices.notificationService.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}