#!/usr/bin/env python3
"""
CI/CD Configuration Validator Script

This script validates CI/CD configurations for the Todo Chatbot application,
checking for proper GitHub Actions workflows, Helm chart configurations,
and deployment readiness.
"""

import os
import yaml
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re


def validate_github_workflow(workflow_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a GitHub Actions workflow file

    Args:
        workflow_path: Path to the workflow YAML file

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        # Check for required top-level fields
        required_fields = ['name', 'on', 'jobs']
        for field in required_fields:
            if field not in workflow:
                issues.append(f"Missing required field: {field}")

        # Validate jobs
        if 'jobs' in workflow:
            jobs = workflow['jobs']
            for job_name, job_config in jobs.items():
                # Check for required job fields
                if 'runs-on' not in job_config:
                    issues.append(f"Job '{job_name}' missing 'runs-on' field")

                # Check for environment usage in production jobs
                if 'production' in job_name.lower() and 'environment' not in job_config:
                    issues.append(f"Production job '{job_name}' should have environment protection")

                # Check for proper dependencies
                if 'needs' in job_config:
                    needs = job_config['needs']
                    if isinstance(needs, str):
                        needs = [needs]

                    for dep in needs:
                        if dep not in jobs:
                            issues.append(f"Job '{job_name}' depends on non-existent job '{dep}'")

        return len(issues) == 0, issues

    except yaml.YAMLError as e:
        return False, [f"YAML parsing error: {str(e)}"]
    except FileNotFoundError:
        return False, [f"Workflow file not found: {workflow_path}"]
    except Exception as e:
        return False, [f"Error validating workflow: {str(e)}"]


def validate_helm_chart(chart_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a Helm chart

    Args:
        chart_path: Path to the Helm chart directory

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Check if required files exist
    required_files = [
        Path(chart_path) / 'Chart.yaml',
        Path(chart_path) / 'values.yaml'
    ]

    for req_file in required_files:
        if not req_file.exists():
            issues.append(f"Missing required file: {req_file}")

    # Validate Chart.yaml
    chart_yaml_path = Path(chart_path) / 'Chart.yaml'
    if chart_yaml_path.exists():
        try:
            with open(chart_yaml_path, 'r') as f:
                chart = yaml.safe_load(f)

            required_chart_fields = ['name', 'version']
            for field in required_chart_fields:
                if field not in chart:
                    issues.append(f"Chart.yaml missing required field: {field}")
        except Exception as e:
            issues.append(f"Error parsing Chart.yaml: {str(e)}")

    # Validate values.yaml
    values_yaml_path = Path(chart_path) / 'values.yaml'
    if values_yaml_path.exists():
        try:
            with open(values_yaml_path, 'r') as f:
                values = yaml.safe_load(f)

            # Check for common deployment configurations
            if 'image' not in values:
                issues.append("values.yaml missing 'image' configuration")
            elif 'repository' not in values.get('image', {}):
                issues.append("values.yaml image configuration missing 'repository'")
            elif 'tag' not in values.get('image', {}):
                issues.append("values.yaml image configuration missing 'tag'")
        except Exception as e:
            issues.append(f"Error parsing values.yaml: {str(e)}")

    # Check for templates directory
    templates_dir = Path(chart_path) / 'templates'
    if not templates_dir.exists():
        issues.append(f"Missing templates directory in chart: {chart_path}")
    else:
        # Check for essential Kubernetes resources
        essential_templates = ['deployment.yaml', 'service.yaml']
        template_files = [f.name.lower() for f in templates_dir.iterdir() if f.is_file()]

        for essential in essential_templates:
            if essential not in template_files:
                issues.append(f"Missing essential template: {essential}")

    return len(issues) == 0, issues


def validate_dockerfile(dockerfile_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a Dockerfile for security and best practices

    Args:
        dockerfile_path: Path to the Dockerfile

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    if not os.path.exists(dockerfile_path):
        return False, [f"Dockerfile not found: {dockerfile_path}"]

    try:
        with open(dockerfile_path, 'r') as f:
            lines = f.readlines()

        dockerfile_content = ''.join(lines).upper()

        # Check for common security issues
        if 'RUN' in dockerfile_content and 'CHMOD 777' in dockerfile_content:
            issues.append("Dockerfile contains insecure chmod 777 command")

        if 'ADD HTTP://' in dockerfile_content or 'ADD HTTPS://' in dockerfile_content:
            issues.append("Dockerfile uses ADD for remote files, should use curl/wget instead")

        # Check for non-root user
        has_non_root_user = any('USER ' in line.upper() and 'ROOT' not in line.upper() for line in lines)
        if not has_non_root_user:
            issues.append("Dockerfile should specify a non-root user for security")

        # Check for minimal base image usage
        has_small_base = any(base in dockerfile_content for base in ['ALPINE', 'SCRATCH', 'DISTROLESS'])
        if not has_small_base:
            issues.append("Consider using a smaller base image (alpine, distroless, scratch)")

        return True, issues

    except Exception as e:
        return False, [f"Error reading Dockerfile: {str(e)}"]


def check_project_structure(project_root: str) -> Tuple[bool, List[str]]:
    """
    Check if the project has the expected structure for CI/CD

    Args:
        project_root: Path to the project root directory

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Required directories
    required_dirs = [
        'backend',
        'frontend',
        'helm',
        '.github/workflows'
    ]

    project_path = Path(project_root)
    for req_dir in required_dirs:
        if not (project_path / req_dir).exists():
            issues.append(f"Missing required directory: {req_dir}")

    # Required files
    required_files = [
        'backend/Dockerfile',
        'frontend/Dockerfile',
        'backend/requirements.txt',
        'frontend/package.json'
    ]

    for req_file in required_files:
        if not (project_path / req_file).exists():
            issues.append(f"Missing required file: {req_file}")

    # Check for Helm charts
    helm_path = project_path / 'helm'
    if helm_path.exists():
        chart_dirs = [d for d in helm_path.iterdir() if d.is_dir()]
        if not chart_dirs:
            issues.append("No Helm charts found in helm/ directory")
        else:
            for chart_dir in chart_dirs:
                chart_yaml = chart_dir / 'Chart.yaml'
                if not chart_yaml.exists():
                    issues.append(f"Missing Chart.yaml in Helm chart: {chart_dir.name}")

    return len(issues) == 0, issues


def validate_ci_configuration(project_root: str = ".") -> Dict[str, any]:
    """
    Validate the entire CI/CD configuration

    Args:
        project_root: Path to the project root directory

    Returns:
        Dictionary with validation results
    """
    results = {
        "project_structure": {"valid": False, "issues": []},
        "workflows": {"valid": False, "issues": [], "count": 0},
        "helm_charts": {"valid": False, "issues": [], "count": 0},
        "dockerfiles": {"valid": False, "issues": [], "count": 0},
        "overall_score": 0
    }

    # Validate project structure
    struct_valid, struct_issues = check_project_structure(project_root)
    results["project_structure"]["valid"] = struct_valid
    results["project_structure"]["issues"] = struct_issues

    # Validate GitHub workflows
    workflow_dir = Path(project_root) / ".github" / "workflows"
    workflow_issues = []
    workflow_count = 0

    if workflow_dir.exists():
        for workflow_file in workflow_dir.glob("*.yml"):
            valid, issues = validate_github_workflow(str(workflow_file))
            if not valid:
                workflow_issues.extend([f"{workflow_file.name}: {issue}" for issue in issues])
            workflow_count += 1

    results["workflows"]["valid"] = len(workflow_issues) == 0
    results["workflows"]["issues"] = workflow_issues
    results["workflows"]["count"] = workflow_count

    # Validate Helm charts
    helm_dir = Path(project_root) / "helm"
    helm_issues = []
    helm_count = 0

    if helm_dir.exists():
        for chart_dir in helm_dir.iterdir():
            if chart_dir.is_dir():
                valid, issues = validate_helm_chart(str(chart_dir))
                if not valid:
                    helm_issues.extend([f"{chart_dir.name}: {issue}" for issue in issues])
                helm_count += 1

    results["helm_charts"]["valid"] = len(helm_issues) == 0
    results["helm_charts"]["issues"] = helm_issues
    results["helm_charts"]["count"] = helm_count

    # Validate Dockerfiles
    dockerfile_paths = [
        Path(project_root) / "backend" / "Dockerfile",
        Path(project_root) / "frontend" / "Dockerfile",
        Path(project_root) / "mcp-server" / "Dockerfile"
    ]

    dockerfile_issues = []
    dockerfile_count = 0

    for dockerfile_path in dockerfile_paths:
        if dockerfile_path.exists():
            valid, issues = validate_dockerfile(str(dockerfile_path))
            if not valid:
                dockerfile_issues.extend([f"{dockerfile_path.name}: {issue}" for issue in issues])
            dockerfile_count += 1

    results["dockerfiles"]["valid"] = len(dockerfile_issues) == 0
    results["dockerfiles"]["issues"] = dockerfile_issues
    results["dockerfiles"]["count"] = dockerfile_count

    # Calculate overall score
    total_checks = 4  # project structure, workflows, helm charts, dockerfiles
    passed_checks = sum([
        results["project_structure"]["valid"],
        results["workflows"]["valid"],
        results["helm_charts"]["valid"],
        results["dockerfiles"]["valid"]
    ])

    results["overall_score"] = int((passed_checks / total_checks) * 100)

    return results


def main():
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."

    print(f"Validating CI/CD configuration for project: {os.path.abspath(project_root)}")
    print("=" * 60)

    results = validate_ci_configuration(project_root)

    # Print results
    print("\n📊 VALIDATION RESULTS")
    print("-" * 30)

    print(f"Overall Score: {results['overall_score']}/100")
    print()

    # Project structure
    struct_status = "✅ PASS" if results["project_structure"]["valid"] else "❌ FAIL"
    print(f"Project Structure: {struct_status}")
    if results["project_structure"]["issues"]:
        for issue in results["project_structure"]["issues"]:
            print(f"  • {issue}")
    print()

    # Workflows
    workflow_status = "✅ PASS" if results["workflows"]["valid"] else "❌ FAIL"
    print(f"GitHub Workflows ({results['workflows']['count']}): {workflow_status}")
    if results["workflows"]["issues"]:
        for issue in results["workflows"]["issues"]:
            print(f"  • {issue}")
    print()

    # Helm charts
    helm_status = "✅ PASS" if results["helm_charts"]["valid"] else "❌ FAIL"
    print(f"Helm Charts ({results['helm_charts']['count']}): {helm_status}")
    if results["helm_charts"]["issues"]:
        for issue in results["helm_charts"]["issues"]:
            print(f"  • {issue}")
    print()

    # Dockerfiles
    dockerfile_status = "✅ PASS" if results["dockerfiles"]["valid"] else "❌ FAIL"
    print(f"Dockerfiles ({results['dockerfiles']['count']}): {dockerfile_status}")
    if results["dockerfiles"]["issues"]:
        for issue in results["dockerfiles"]["issues"]:
            print(f"  • {issue}")
    print()

    # Summary
    print("📋 SUMMARY")
    print("-" * 30)
    if results['overall_score'] >= 90:
        print("🎉 Excellent! CI/CD configuration is ready for production.")
    elif results['overall_score'] >= 70:
        print("👍 Good! Most CI/CD configuration is in place, but some issues need attention.")
    elif results['overall_score'] >= 50:
        print("⚠️  Needs work! Several CI/CD configuration issues need to be addressed.")
    else:
        print("❌ Major issues! Significant CI/CD configuration work is needed.")

    # Exit with error code if validation failed
    if results['overall_score'] < 70:
        sys.exit(1)


if __name__ == "__main__":
    main()