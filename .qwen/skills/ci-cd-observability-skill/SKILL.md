---
name: ci-cd-observability-skill
description: Continuous integration, deployment, and observability. Create GitHub Actions pipeline for Minikube → Oracle OKE deployment. Automate Helm chart deployments and environment promotions. Ensure monitoring/logging hooks, resource checks, and failure handling. Collaborate with context-verifier-agent to use latest CI/CD practices. Follow Phase V constitution and AI-assisted no-manual-coding workflow.
---

# CI/CD Observability Skill

## Overview
This skill provides guidance for implementing continuous integration, deployment, and observability practices for the Todo Chatbot application. It focuses on creating automated GitHub Actions pipelines that support deployment from Minikube to Oracle OKE, automating Helm chart deployments, implementing monitoring and logging, and ensuring proper resource management and failure handling.

## When to Use This Skill
Use this skill when:
1. Setting up CI/CD pipelines for the Todo Chatbot application
2. Creating GitHub Actions workflows for automated deployments
3. Implementing environment promotion strategies (Dev → Staging → Production)
4. Configuring monitoring and logging for deployed services
5. Setting up resource checks and failure handling mechanisms
6. Ensuring compliance with Phase V constitution regarding deployment practices
7. Implementing AI-assisted deployment workflows without manual coding

## Prerequisites
- GitHub repository with the Todo Chatbot application
- Access to Oracle OKE cluster for production deployments
- Helm charts for all application services
- Monitoring and logging infrastructure (Prometheus, Grafana, ELK stack, etc.)
- Access to context-verifier-agent for latest CI/CD practices

## Core Responsibilities

### 1. GitHub Actions Pipeline Creation
- Create automated workflows for:
  - Code validation and testing
  - Container image building and publishing
  - Helm chart packaging and publishing
  - Deployment to different environments
  - Post-deployment validation and monitoring

### 2. Environment Promotion Automation
- Implement automated promotion from Minikube (development) to Oracle OKE (production)
- Set up different environments (Dev, Staging, Production) with appropriate configurations
- Ensure proper configuration management across environments
- Implement safe deployment practices (blue-green, canary, rolling updates)

### 3. Monitoring and Logging Implementation
- Set up application and infrastructure monitoring
- Implement centralized logging for all services
- Configure alerting for critical issues
- Establish observability dashboards for system health

### 4. Resource Management and Failure Handling
- Implement resource checks to prevent over-provisioning
- Set up failure handling mechanisms with proper rollbacks
- Configure health checks and liveness/readiness probes
- Implement circuit breaker patterns for resilience

## Architecture Guidelines

### CI/CD Pipeline Principles
1. **Automation First**: All deployment steps should be automated with no manual intervention required
2. **Environment Parity**: Maintain consistent configurations across all environments
3. **Immutable Builds**: Build artifacts once and promote them across environments
4. **Fast Feedback**: Provide quick feedback on build and test failures
5. **Security**: Implement security scanning at every stage of the pipeline

### Deployment Strategies
1. **Blue-Green Deployment**: Minimize downtime during deployments
2. **Canary Releases**: Gradually roll out changes to a subset of users
3. **Rolling Updates**: Incrementally update application instances
4. **Rollback Capability**: Maintain ability to quickly revert to previous versions

### Observability Standards
1. **Centralized Logging**: All application logs should be aggregated in a central location
2. **Distributed Tracing**: Implement tracing across all services
3. **Metrics Collection**: Collect key performance indicators for all services
4. **Alerting**: Set up alerts for critical system metrics and errors

## Implementation Steps

### 1. Pipeline Design Phase
1. Identify all required pipeline stages (build, test, package, deploy)
2. Define environment-specific configurations
3. Plan promotion strategy between environments
4. Set up monitoring and alerting requirements

### 2. Infrastructure Setup
1. Configure GitHub Actions runners
2. Set up container registry for Docker images
3. Configure Helm chart repository
4. Set up monitoring and logging infrastructure

### 3. Pipeline Implementation
1. Create GitHub Actions workflow files
2. Implement build and test steps
3. Set up artifact publishing (Docker images, Helm charts)
4. Configure deployment steps for each environment

### 4. Validation and Monitoring
1. Test pipeline with sample deployments
2. Verify monitoring and logging are working
3. Test failure scenarios and rollback procedures
4. Ensure all operations comply with Phase V constitution

## GitHub Actions Workflow Examples

### Main CI/CD Pipeline (.github/workflows/ci-cd-pipeline.yml)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt

    - name: Run tests
      run: |
        pytest backend/tests/

    - name: Run linting
      run: |
        flake8 backend/

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push frontend
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        file: ./frontend/Dockerfile
        push: true
        tags: |
          ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
          ghcr.io/${{ github.repository }}/frontend:latest

    - name: Build and push backend
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./backend/Dockerfile
        push: true
        tags: |
          ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
          ghcr.io/${{ github.repository }}/backend:latest

    - name: Build and push MCP server
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./mcp-server/Dockerfile
        push: true
        tags: |
          ghcr.io/${{ github.repository }}/mcp-server:${{ github.sha }}
          ghcr.io/${{ github.repository }}/mcp-server:latest

  deploy-dev:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: development
    steps:
    - uses: actions/checkout@v4

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Set up Helm
      uses: azure/setup-helm@v3
      with:
        version: 'latest'

    - name: Configure KUBECONFIG
      run: |
        echo "${{ secrets.KUBECONFIG_DEV }}" | base64 -d > kubeconfig
        export KUBECONFIG=$PWD/kubeconfig

    - name: Deploy with Helm
      run: |
        helm upgrade --install todo-frontend ./helm/todo-frontend \
          --set image.repository=ghcr.io/${{ github.repository }}/frontend \
          --set image.tag=${{ github.sha }} \
          --namespace todo-app --create-namespace \
          --wait

        helm upgrade --install todo-backend ./helm/todo-backend \
          --set image.repository=ghcr.io/${{ github.repository }}/backend \
          --set image.tag=${{ github.sha }} \
          --namespace todo-app \
          --wait

        helm upgrade --install mcp-server ./helm/mcp-server \
          --set image.repository=ghcr.io/${{ github.repository }}/mcp-server \
          --set image.tag=${{ github.sha }} \
          --namespace todo-app \
          --wait
```

## Best Practices

### Security
- Store all secrets in GitHub repository secrets
- Use OIDC tokens for authentication where possible
- Scan Docker images for vulnerabilities
- Implement branch protection rules

### Performance
- Use caching to speed up builds
- Parallelize independent jobs
- Optimize Docker image sizes
- Implement proper resource limits

### Reliability
- Implement proper error handling and retries
- Use timeouts for long-running operations
- Set up notifications for pipeline failures
- Maintain pipeline health metrics

### Observability
- Log all pipeline activities
- Monitor deployment metrics
- Track deployment frequency and lead time
- Implement deployment health checks

## Multi-Environment Considerations

### Environment-Specific Configurations
- Development: Faster deployments, detailed logging
- Staging: Full testing, performance validation
- Production: Safe deployment strategies, extensive monitoring

### Promotion Strategy
- Automated promotion between dev and staging
- Manual approval for production promotion
- Blue-green or canary deployments for production
- Rollback procedures for failed deployments

### Validation Checklist
- [ ] GitHub Actions workflows configured
- [ ] Container images published to registry
- [ ] Helm charts published and versioned
- [ ] Deployments successful in all environments
- [ ] Monitoring and logging configured
- [ ] Health checks passing
- [ ] Security scans passed
- [ ] Compliance with Phase V constitution verified

## Phase V Constitution Compliance

This skill ensures compliance with:
- **XXVII. CI/CD and Observability Law**: GitHub Actions pipelines for deployment automation
- **XXVI. Cloud Deployment Law**: Automated deployment to Oracle OKE
- **XXVIII. AI-Assisted DevOps Enhancement Law**: Automated deployment workflows
- **XXI. Infrastructure as Code Law**: Helm chart deployment automation
- **XVIII. Kubernetes Deployment Law**: Automated Kubernetes deployments

## Common Commands and Operations

### Using context-verifier-agent
- Get latest CI/CD best practices: `context-verifier-agent get cicd-best-practices --version latest`
- Validate pipeline configuration: `context-verifier-agent validate pipeline --against phase-v-constitution`
- Check security compliance: `context-verifier-agent check security --pipeline github-actions`

### Pipeline Management
- Trigger deployment manually: `gh workflow run "Deploy to Production"`
- Check pipeline status: `gh run list --workflow="ci-cd-pipeline.yml"`
- View pipeline logs: `gh run view <run-id> --log`

## Troubleshooting

### Common Issues
1. **Authentication Failures**: Verify OIDC setup and secret configurations
2. **Image Pull Errors**: Check container registry access and image tags
3. **Helm Deployment Failures**: Validate chart configurations and Kubernetes connectivity
4. **Resource Limit Issues**: Adjust resource limits based on environment capacity

### Diagnostic Commands
- Check GitHub Actions runner status: `gh api repos/:owner/:repo/actions/runners`
- View deployment status: `kubectl get pods -n todo-app`
- Check Helm release status: `helm status <release-name> -n todo-app`
- Monitor pipeline metrics: Use configured monitoring tools