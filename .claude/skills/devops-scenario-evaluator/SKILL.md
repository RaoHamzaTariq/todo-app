---
name: devops-scenario-evaluator
description: Diagnose common Kubernetes issues including CrashLoopBackOff, ImagePullBackOff, Pending pods, and Resource saturation. Suggest kubectl-ai natural language commands, kagent resource optimization checks, and provide expected resolution steps. Use when troubleshooting Kubernetes deployments, analyzing pod failures, or investigating resource constraints.
---

# DevOps Scenario Evaluator

## Overview

This skill teaches Claude how to diagnose common Kubernetes issues and suggest appropriate remediation steps using AI-assisted tools like kubectl-ai and kagent.

## When to Use This Skill

Use this skill when:
- Pods are in CrashLoopBackOff state
- Pods show ImagePullBackOff errors
- Pods remain in Pending state
- Resource saturation (CPU/memory) is suspected
- Investigating deployment failures
- Performing routine health checks on Kubernetes clusters
- Troubleshooting application availability issues

## Conditions, Signals, and Actions Framework

### 1. CrashLoopBackOff Diagnosis

**Condition**: Pod is restarting continuously in a loop

**Signals**:
- Pod status shows `CrashLoopBackOff`
- Multiple restarts recorded in pod status
- Container logs show repeated startup failures

**Actions**:
1. Use kubectl-ai to analyze failing pods:
   ```
   kubectl-ai diagnose failing pods
   ```
2. Check container logs:
   ```
   kubectl-ai show logs for pods with CrashLoopBackOff
   ```
3. Inspect pod events:
   ```
   kubectl-ai describe pods with CrashLoopBackOff
   ```
4. Verify resource limits are adequate:
   ```
   kubectl-ai check resources for failing pods
   ```
5. Suggest kagent analysis:
   ```
   kagent analyze pod-resource conflicts
   ```

### 2. ImagePullBackOff Diagnosis

**Condition**: Pod cannot pull the specified container image

**Signals**:
- Pod status shows `ImagePullBackOff`
- Error message indicates image pull failure
- Registry authentication issues

**Actions**:
1. Use kubectl-ai to identify problematic pods:
   ```
   kubectl-ai find pods with ImagePullBackOff
   ```
2. Check image configuration:
   ```
   kubectl-ai verify image configuration for pods
   ```
3. Validate image pull secrets:
   ```
   kubectl-ai check image pull secrets
   ```
4. Test registry connectivity:
   ```
   kubectl-ai test registry connectivity
   ```
5. Suggest kagent checks:
   ```
   kagent validate registry access
   ```

### 3. Pending Pod Diagnosis

**Condition**: Pod remains in Pending state and is not scheduled

**Signals**:
- Pod status shows `Pending`
- No nodes available to schedule the pod
- Resource constraints preventing scheduling

**Actions**:
1. Use kubectl-ai to analyze pending pods:
   ```
   kubectl-ai diagnose pending pods
   ```
2. Check node resources:
   ```
   kubectl-ai show node resource usage
   ```
3. Analyze scheduling constraints:
   ```
   kubectl-ai explain why pods are pending
   ```
4. Identify node selector issues:
   ```
   kubectl-ai check node selectors and affinities
   ```
5. Suggest kagent optimization:
   ```
   kagent analyze node scheduling constraints
   ```

### 4. Resource Saturation Diagnosis

**Condition**: High CPU or memory usage affecting cluster performance

**Signals**:
- High resource utilization across multiple nodes
- Pods being evicted due to resource pressure
- Performance degradation symptoms

**Actions**:
1. Use kubectl-ai to analyze resource pressure:
   ```
   kubectl-ai analyze resource pressure
   ```
2. Check cluster resource usage:
   ```
   kubectl-ai show cluster resource usage
   ```
3. Identify resource hogs:
   ```
   kubectl-ai find pods consuming high resources
   ```
4. Examine namespace usage:
   ```
   kubectl-ai show resource usage by namespace
   ```
5. Suggest kagent optimization:
   ```
   kagent optimize resource allocation
   ```

## Step-by-Step Diagnostic Process

### Step 1: Initial Assessment
1. Identify the specific issue type from the condition
2. Gather basic cluster information:
   ```
   kubectl-ai show cluster status
   ```
3. List affected pods:
   ```
   kubectl-ai show pods with issues
   ```

### Step 2: Detailed Analysis
1. For each affected pod, examine:
   - Current status and events
   - Resource configuration
   - Image configuration
   - Node assignment (if applicable)

2. Use appropriate kubectl-ai commands based on the issue:
   - For crashes: `kubectl-ai diagnose crash reasons`
   - For image issues: `kubectl-ai verify image integrity`
   - For pending: `kubectl-ai analyze scheduling`
   - For resource issues: `kubectl-ai analyze usage patterns`

### Step 3: Root Cause Identification
1. Correlate findings from multiple diagnostic commands
2. Identify patterns or common causes
3. Prioritize issues based on severity and impact

### Step 4: Remediation Strategy
1. Propose specific fixes based on identified root causes
2. Suggest preventive measures to avoid recurrence
3. Recommend monitoring enhancements if needed

## Examples of Commands and Expected Outputs

### Example 1: CrashLoopBackOff Investigation
```
Command: kubectl-ai diagnose failing pods
Expected Output: Lists pods in CrashLoopBackOff with restart counts and potential reasons
```

### Example 2: Resource Pressure Analysis
```
Command: kubectl-ai analyze resource pressure
Expected Output: Shows nodes with high CPU/memory usage, identifies resource-hungry pods
```

### Example 3: Image Pull Issues
```
Command: kubectl-ai check image pull secrets
Expected Output: Validates image pull secrets and their association with pods
```

### Example 4: Pending Pod Analysis
```
Command: kubectl-ai explain why pods are pending
Expected Output: Details scheduling constraints and resource availability issues
```

## Guidance for Log Inspection

When initial diagnostics indicate the need for deeper inspection:

### Container Logs
1. Focus on the most recent startup attempts
2. Look for configuration errors, missing dependencies, or connection failures
3. Check for resource exhaustion errors (out of memory, etc.)

### Event Logs
1. Review pod events for scheduling-related issues
2. Check for node-related problems (disk pressure, memory pressure)
3. Identify quota or limit violations

### System Logs
1. Examine kubelet logs on affected nodes if possible
2. Check for resource contention or hardware issues
3. Verify network connectivity and DNS resolution

## Expected Resolution Steps by Issue Type

### CrashLoopBackOff Resolutions
1. Adjust resource limits/requests
2. Fix application configuration issues
3. Address dependency problems
4. Correct entrypoint/command issues

### ImagePullBackOff Resolutions
1. Verify image name and tag correctness
2. Update image pull secrets
3. Check registry accessibility and credentials
4. Ensure proper registry authentication

### Pending Pod Resolutions
1. Scale up cluster capacity
2. Adjust resource requests/limits
3. Modify node selectors or taints/tolerations
4. Remove resource quotas if overly restrictive

### Resource Saturation Resolutions
1. Optimize resource requests/limits
2. Scale up cluster or add nodes
3. Implement resource quotas and limits
4. Adjust application resource consumption

## Integration with AI Tools

### kubectl-ai Integration
- Use natural language queries for complex diagnostics
- Leverage AI pattern recognition for anomaly detection
- Request automated remediation suggestions

### kagent Integration
- Perform intelligent resource optimization
- Execute automated scaling decisions
- Implement predictive maintenance actions

## Validation Steps After Remediation
1. Verify pod status has changed from error state
2. Confirm application functionality is restored
3. Monitor resource usage to ensure stability
4. Validate that no new issues were introduced