# Example Deployments for k8s-deployment-orchestrator

This directory contains complete example deployments for different service types.

## Frontend (Next.js) Example

### frontend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: my-registry/nextjs-frontend:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: frontend-config
              key: api_url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### frontend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  labels:
    app: frontend
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

## Backend (FastAPI) Example

### backend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: my-registry/fastapi-backend:v1.0.0
        ports:
        - containerPort: 8000
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
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api_key
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### backend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  labels:
    app: backend
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

## MCP Server Example

### mcp-server-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  labels:
    app: mcp-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: my-registry/mcp-server:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: MCP_PORT
          value: "3000"
        - name: MCP_CONFIG_PATH
          value: "/etc/mcp/config.yaml"
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### mcp-server-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mcp-server-service
  labels:
    app: mcp-server
spec:
  selector:
    app: mcp-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

## Complete Helm Chart Example

### Chart.yaml
```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for the Todo App
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### values.yaml
```yaml
# Global configuration
global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

# Frontend configuration
frontend:
  replicaCount: 2
  image:
    repository: my-registry/nextjs-frontend
    pullPolicy: IfNotPresent
    tag: "v1.0.0"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi
  env:
    NEXT_PUBLIC_API_URL: "http://backend-service:80"

# Backend configuration
backend:
  replicaCount: 2
  image:
    repository: my-registry/fastapi-backend
    pullPolicy: IfNotPresent
    tag: "v1.0.0"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi

# MCP Server configuration
mcpServer:
  replicaCount: 1
  image:
    repository: my-registry/mcp-server
    pullPolicy: IfNotPresent
    tag: "v1.0.0"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi
```