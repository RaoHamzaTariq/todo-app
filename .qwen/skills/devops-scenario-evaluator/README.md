# DevOps Scenario Evaluator Skill

## Overview
The devops-scenario-evaluator skill provides comprehensive guidance for diagnosing common Kubernetes issues including CrashLoopBackOff, ImagePullBackOff, Pending pods, and Resource saturation. The skill suggests appropriate kubectl-ai natural language commands, kagent resource optimization checks, and provides expected resolution steps.

## Components

### Core Skill
- **SKILL.md**: Main skill definition with conditions, signals, and actions framework for troubleshooting

### References
- **troubleshooting-checklist.md**: Detailed checklist for systematic troubleshooting

### Scripts
- **diagnose-cluster-health.sh**: Comprehensive cluster health diagnostics
- **analyze-pod-failures.sh**: Detailed analysis of specific pod failures

## Key Features

1. **Issue-Specific Diagnostics**: Targeted troubleshooting for common Kubernetes issues
2. **AI Tool Integration**: Guidance for using kubectl-ai and kagent effectively
3. **Systematic Approach**: Structured methodology for root cause analysis
4. **Actionable Recommendations**: Clear resolution steps for each issue type
5. **Verification Steps**: Post-fix validation procedures

## Usage Scenarios

This skill is ideal for:
- Troubleshooting Kubernetes deployments
- Analyzing pod failures (CrashLoopBackOff, ImagePullBackOff)
- Investigating scheduling issues (Pending pods)
- Resolving resource saturation problems
- Performing routine cluster health checks

The skill follows best practices for Kubernetes troubleshooting and integrates well with AI-assisted DevOps tools.