# Kubernetes Troubleshooting Checklist

## Pre-Diagnosis Preparation

### 1. Environment Verification
- [ ] Confirm kubectl access to the cluster
- [ ] Verify cluster connectivity and basic functionality
- [ ] Check current namespace context
- [ ] Validate permissions for diagnostic operations

### 2. Information Gathering
- [ ] Identify affected pods/nodes
- [ ] Note timestamps of when issues started
- [ ] Document any recent changes to the environment
- [ ] Collect application error messages or symptoms

## Issue-Specific Checklists

### CrashLoopBackOff Checklist

#### 1. Container Health Check
- [ ] Check container logs for startup errors
- [ ] Verify application configuration files
- [ ] Validate environment variables and secrets
- [ ] Confirm correct entrypoint and command

#### 2. Resource Constraints
- [ ] Verify CPU and memory requests/limits
- [ ] Check for OutOfMemory (OOM) kills in logs
- [ ] Validate resource availability on target nodes
- [ ] Review horizontal pod autoscaler (HPA) settings

#### 3. Dependency Issues
- [ ] Confirm database connections
- [ ] Verify external service dependencies
- [ ] Check file system permissions
- [ ] Validate mounted volumes and configurations

### ImagePullBackOff Checklist

#### 1. Image Configuration
- [ ] Verify image name and tag spelling
- [ ] Confirm registry URL is correct
- [ ] Check if image exists in registry
- [ ] Validate image digest if used

#### 2. Authentication
- [ ] Verify image pull secret exists
- [ ] Confirm secret is correctly referenced in pod spec
- [ ] Check registry credentials in secret
- [ ] Validate secret permissions

#### 3. Network Connectivity
- [ ] Test registry accessibility from cluster
- [ ] Check firewall rules and network policies
- [ ] Verify DNS resolution for registry
- [ ] Confirm proxy settings if applicable

### Pending Pod Checklist

#### 1. Node Availability
- [ ] Check if sufficient nodes exist in cluster
- [ ] Verify node status and health
- [ ] Confirm node resources are available
- [ ] Check for cordoned or unschedulable nodes

#### 2. Resource Constraints
- [ ] Validate resource requests vs available capacity
- [ ] Check namespace resource quotas
- [ ] Verify persistent volume availability
- [ ] Confirm storage class configuration

#### 3. Scheduling Constraints
- [ ] Review node selectors and labels
- [ ] Check node affinity/anti-affinity rules
- [ ] Verify taints and tolerations
- [ ] Validate topology spread constraints

### Resource Saturation Checklist

#### 1. CPU Saturation
- [ ] Identify high CPU consumption pods
- [ ] Check for CPU-intensive processes
- [ ] Review CPU limits and throttling
- [ ] Validate CPU quota usage

#### 2. Memory Saturation
- [ ] Identify high memory consumption pods
- [ ] Check for memory leaks or growth patterns
- [ ] Review memory limits and OOM kills
- [ ] Validate memory quota usage

#### 3. Node-Level Pressure
- [ ] Check for disk pressure conditions
- [ ] Verify memory pressure on nodes
- [ ] Review ephemeral storage usage
- [ ] Confirm node resource allocation

## Diagnostic Command Sequences

### General Investigation Sequence
1. `kubectl-ai show cluster status`
2. `kubectl-ai show pods with issues`
3. `kubectl-ai show node resource usage`
4. `kubectl-ai describe affected pods`
5. `kubectl-ai show pod events`

### CrashLoopBackOff Investigation Sequence
1. `kubectl-ai diagnose failing pods`
2. `kubectl-ai show logs for crashing pods`
3. `kubectl-ai check pod resource limits`
4. `kubectl-ai verify container configuration`
5. `kubectl-ai analyze startup sequence`

### ImagePullBackOff Investigation Sequence
1. `kubectl-ai find pods with ImagePullBackOff`
2. `kubectl-ai verify image configuration`
3. `kubectl-ai check image pull secrets`
4. `kubectl-ai test registry connectivity`
5. `kubectl-ai validate registry access`

### Pending Pod Investigation Sequence
1. `kubectl-ai diagnose pending pods`
2. `kubectl-ai analyze scheduling constraints`
3. `kubectl-ai show node availability`
4. `kubectl-ai check resource quotas`
5. `kubectl-ai verify node requirements`

## Resolution Verification Steps

### Post-Fix Validation
- [ ] Confirm pod status has changed from error state
- [ ] Verify application functionality is restored
- [ ] Check resource usage is within acceptable ranges
- [ ] Validate no new issues were introduced
- [ ] Confirm monitoring alerts are cleared

### Preventive Measures
- [ ] Document root cause and resolution
- [ ] Implement monitoring for similar issues
- [ ] Add resource limits where missing
- [ ] Update deployment templates with lessons learned
- [ ] Schedule periodic resource capacity reviews