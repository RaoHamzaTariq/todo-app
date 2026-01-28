# Data Model: Phase IV Kubernetes Deployment

## Kubernetes Entities

### Deployment
**Description**: Kubernetes resource that manages application pods for each service
**Fields**:
- `apiVersion`: apps/v1 (standard API version)
- `kind`: Deployment (resource type)
- `metadata.name`: Service-specific name (frontend, backend, mcp-server)
- `metadata.namespace`: Namespace for the deployment (default or specified)
- `spec.replicas`: Number of desired pods (typically 1 for Minikube)
- `spec.selector.matchLabels`: Labels to match pods
- `spec.template.metadata.labels`: Labels for pods
- `spec.template.spec.containers[]`: Container specifications
- `spec.template.spec.containers[].name`: Container name
- `spec.template.spec.containers[].image`: Docker image reference
- `spec.template.spec.containers[].ports[]`: Port configurations
- `spec.template.spec.containers[].envFrom[]`: Environment from ConfigMaps/Secrets
- `spec.template.spec.containers[].resources`: Resource limits and requests
- `spec.template.spec.containers[].livenessProbe`: Health check configuration
- `spec.template.spec.containers[].readinessProbe`: Readiness check configuration

**Relationships**:
- Owned by: Helm Chart
- Connects to: Service resource

**Validation rules**:
- Image must be a valid container image reference
- Ports must be within valid range (1-65535)
- Resource requests must not exceed limits

### Service
**Description**: Kubernetes resource that enables internal networking between services
**Fields**:
- `apiVersion`: v1 (standard API version)
- `kind`: Service (resource type)
- `metadata.name`: Service-specific name (frontend-svc, backend-svc, mcp-svc)
- `metadata.namespace`: Namespace for the service
- `spec.selector`: Selector to match pods
- `spec.ports[]`: Port configurations
- `spec.type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `spec.clusterIP`: Internal IP address (for ClusterIP type)

**Relationships**:
- Owned by: Helm Chart
- Connects to: Deployment resource

**Validation rules**:
- Selector must match labels in corresponding Deployment
- Port must match container port in corresponding Deployment

### Ingress
**Description**: Kubernetes resource that provides external access to the frontend service
**Fields**:
- `apiVersion`: networking.k8s.io/v1 (standard API version)
- `kind`: Ingress (resource type)
- `metadata.name`: Ingress name (e.g., todo-app-ingress)
- `metadata.namespace`: Namespace for the ingress
- `spec.rules[]`: Routing rules
- `spec.rules[].host`: Hostname for routing
- `spec.rules[].http.paths[]`: Path-based routing
- `spec.rules[].http.paths[].path`: URL path
- `spec.rules[].http.paths[].pathType`: Path matching type (Exact, Prefix)
- `spec.rules[].http.paths[].backend.service.name`: Backend service name
- `spec.rules[].http.paths[].backend.service.port.number`: Backend port

**Relationships**:
- Owned by: Helm Chart
- Connects to: Service resource

**Validation rules**:
- Paths must be valid URL paths
- Backend services must exist
- Hostnames must be valid

### ConfigMap
**Description**: Kubernetes resource that stores non-sensitive configuration data
**Fields**:
- `apiVersion`: v1 (standard API version)
- `kind`: ConfigMap (resource type)
- `metadata.name`: ConfigMap name
- `metadata.namespace`: Namespace for the ConfigMap
- `data`: Key-value pairs of configuration data

**Relationships**:
- Owned by: Helm Chart
- Referenced by: Deployment resource

**Validation rules**:
- Keys must be valid identifiers
- Values must be strings

### Secret
**Description**: Kubernetes resource that stores sensitive data like credentials and keys
**Fields**:
- `apiVersion`: v1 (standard API version)
- `kind`: Secret (resource type)
- `metadata.name`: Secret name
- `metadata.namespace`: Namespace for the Secret
- `type`: Secret type (Opaque, kubernetes.io/tls, etc.)
- `data`: Base64-encoded key-value pairs of sensitive data
- `stringData`: Plaintext key-value pairs (encoded automatically)

**Relationships**:
- Owned by: Helm Chart
- Referenced by: Deployment resource

**Validation rules**:
- Sensitive data must be properly encoded
- Keys must be valid identifiers

### PersistentVolume
**Description**: Kubernetes resource that provides durable storage for the database
**Fields**:
- `apiVersion`: v1 (standard API version)
- `kind`: PersistentVolume (resource type)
- `metadata.name`: PV name
- `metadata.namespace`: Namespace for the PV (optional)
- `spec.capacity.storage`: Storage capacity (e.g., 10Gi)
- `spec.accessModes[]`: Access modes (ReadWriteOnce, ReadOnlyMany, etc.)
- `spec.hostPath.path`: Path on the host node (for Minikube)
- `spec.persistentVolumeReclaimPolicy`: Reclaim policy (Retain, Recycle, Delete)

**Relationships**:
- Owned by: Helm Chart
- Claimed by: PersistentVolumeClaim

**Validation rules**:
- Capacity must be sufficient for expected data
- Access modes must be compatible with workload requirements

### PersistentVolumeClaim
**Description**: Kubernetes resource that requests storage from PersistentVolumes
**Fields**:
- `apiVersion`: v1 (standard API version)
- `kind`: PersistentVolumeClaim (resource type)
- `metadata.name`: PVC name
- `metadata.namespace`: Namespace for the PVC
- `spec.accessModes[]`: Requested access modes
- `spec.resources.requests.storage`: Requested storage capacity

**Relationships**:
- Owned by: Helm Chart
- Claims: PersistentVolume

**Validation rules**:
- Requested capacity must not exceed available PV capacity
- Access modes must be supported by available PVs

## Helm Chart Entities

### Chart.yaml
**Description**: Metadata file for Helm chart
**Fields**:
- `apiVersion`: Helm API version (v2)
- `name`: Chart name
- `version`: Chart version
- `appVersion`: Application version
- `description`: Chart description
- `dependencies[]`: Chart dependencies

**Relationships**:
- Belongs to: Helm Chart
- Defines: Entire chart structure

### values.yaml
**Description**: Default configuration values for Helm chart
**Fields**:
- `image.repository`: Container image repository
- `image.tag`: Container image tag
- `image.pullPolicy`: Image pull policy
- `service.type`: Service type
- `service.port`: Service port
- `ingress.enabled`: Whether to enable ingress
- `ingress.className`: Ingress class name
- `ingress.hosts[]`: Ingress hosts
- `resources.limits.cpu`: CPU limit
- `resources.limits.memory`: Memory limit
- `resources.requests.cpu`: CPU request
- `resources.requests.memory`: Memory request
- `nodeSelector`: Node selection constraints
- `tolerations`: Taint tolerations
- `affinity`: Pod affinity/anti-affinity rules

**Relationships**:
- Belongs to: Helm Chart
- Configures: All deployed resources

### templates/deployment.yaml
**Description**: Template for Deployment resource
**Fields**:
- Template parameters that map to values.yaml
- Standard Deployment resource structure

**Relationships**:
- Belongs to: Helm Chart
- Generates: Deployment resource

### templates/service.yaml
**Description**: Template for Service resource
**Fields**:
- Template parameters that map to values.yaml
- Standard Service resource structure

**Relationships**:
- Belongs to: Helm Chart
- Generates: Service resource

## State Transitions

### Deployment State Transitions
- `Pending` → `Running` → `Terminating` → `Deleted`
- `Running` → `Failed` (on container failure)
- `Running` → `Succeeded` (for jobs)

### Pod State Transitions (within Deployment)
- `Pending` → `ContainerCreating` → `Running` → `Terminated`
- `Running` → `CrashLoopBackOff` (on repeated failures)
- `Running` → `ImagePullBackOff` (on image pull failures)