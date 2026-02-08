#!/usr/bin/env python3
"""
Dapr Configuration Validator Script

This script validates Dapr component configurations against the expected schema
and checks for common issues in the Todo Chatbot application setup.
"""

import yaml
import json
import sys
from jsonschema import validate, ValidationError
from typing import Dict, List, Any

# Define schemas for different Dapr component types
COMPONENT_SCHEMAS = {
    "pubsub.kafka": {
        "type": "object",
        "properties": {
            "apiVersion": {"type": "string"},
            "kind": {"type": "string", "enum": ["Component"]},
            "metadata": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
            "spec": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "pattern": "^pubsub\\.kafka$"},
                    "version": {"type": "string"},
                    "metadata": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": ["string", "number", "boolean"]},
                                "secretKeyRef": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "key": {"type": "string"}
                                    },
                                    "required": ["name", "key"]
                                }
                            },
                            "required": ["name"]
                        }
                    }
                },
                "required": ["type", "version", "metadata"]
            }
        },
        "required": ["apiVersion", "kind", "metadata", "spec"]
    },
    "state.redis": {
        "type": "object",
        "properties": {
            "apiVersion": {"type": "string"},
            "kind": {"type": "string", "enum": ["Component"]},
            "metadata": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
            "spec": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "pattern": "^state\\.redis$"},
                    "version": {"type": "string"},
                    "metadata": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": ["string", "number", "boolean"]},
                                "secretKeyRef": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "key": {"type": "string"}
                                    },
                                    "required": ["name", "key"]
                                }
                            },
                            "required": ["name"]
                        }
                    }
                },
                "required": ["type", "version", "metadata"]
            }
        },
        "required": ["apiVersion", "kind", "metadata", "spec"]
    },
    "secretstores.kubernetes": {
        "type": "object",
        "properties": {
            "apiVersion": {"type": "string"},
            "kind": {"type": "string", "enum": ["Component"]},
            "metadata": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
            "spec": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "pattern": "^secretstores\\.kubernetes$"},
                    "version": {"type": "string"},
                    "metadata": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": ["string", "number", "boolean"]},
                                "secretKeyRef": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "key": {"type": "string"}
                                    },
                                    "required": ["name", "key"]
                                }
                            },
                            "required": ["name"]
                        }
                    }
                },
                "required": ["type", "version", "metadata"]
            }
        },
        "required": ["apiVersion", "kind", "metadata", "spec"]
    }
}

def validate_dapr_component(component_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate a single Dapr component configuration

    Args:
        component_data: The parsed YAML/JSON component configuration

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        spec_type = component_data.get('spec', {}).get('type')

        if not spec_type:
            return False, "Missing 'spec.type' field in component"

        if spec_type not in COMPONENT_SCHEMAS:
            return False, f"Unsupported component type: {spec_type}. Supported types: {list(COMPONENT_SCHEMAS.keys())}"

        schema = COMPONENT_SCHEMAS[spec_type]
        validate(instance=component_data, schema=schema)

        # Additional checks specific to each component type
        if spec_type == "pubsub.kafka":
            return validate_kafka_config(component_data)
        elif spec_type == "state.redis":
            return validate_redis_config(component_data)
        elif spec_type == "secretstores.kubernetes":
            return validate_kubernetes_secrets_config(component_data)

        return True, None
    except ValidationError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_kafka_config(component_data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate Kafka-specific configuration requirements"""
    metadata = component_data.get('spec', {}).get('metadata', [])

    # Check for required Kafka properties
    required_props = ['brokers']
    missing_props = []

    for prop in required_props:
        if not any(item.get('name') == prop for item in metadata):
            missing_props.append(prop)

    if missing_props:
        return False, f"Missing required Kafka properties: {missing_props}"

    # Check if auth is properly configured
    auth_required = None
    for item in metadata:
        if item.get('name') == 'authRequired':
            auth_required = item.get('value')
            break

    if auth_required == 'true':
        # Check for auth-related properties
        auth_props = ['saslUsername', 'saslPassword']
        missing_auth_props = []

        for prop in auth_props:
            if not any(item.get('name') == prop for item in metadata):
                missing_auth_props.append(prop)

        if missing_auth_props:
            return False, f"Kafka authentication is required but missing properties: {missing_auth_props}"

    return True, None


def validate_redis_config(component_data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate Redis-specific configuration requirements"""
    metadata = component_data.get('spec', {}).get('metadata', [])

    # Check for required Redis properties
    required_props = ['redisHost']
    missing_props = []

    for prop in required_props:
        if not any(item.get('name') == prop for item in metadata):
            missing_props.append(prop)

    if missing_props:
        return False, f"Missing required Redis properties: {missing_props}"

    return True, None


def validate_kubernetes_secrets_config(component_data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate Kubernetes secrets configuration requirements"""
    # Kubernetes secrets component typically doesn't need specific metadata
    # Just ensure the basic structure is correct
    return True, None


def validate_dapr_sidecar_annotations(annotations: Dict[str, str]) -> tuple[bool, List[str]]:
    """
    Validate Dapr sidecar annotations in Kubernetes deployments

    Args:
        annotations: Dictionary of Kubernetes annotations

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Required annotations for Dapr
    required_annotations = ['dapr.io/enabled', 'dapr.io/app-id']

    for annotation in required_annotations:
        if annotation not in annotations:
            issues.append(f"Missing required annotation: {annotation}")

    # Check if Dapr is enabled
    if annotations.get('dapr.io/enabled') != 'true':
        issues.append("dapr.io/enabled should be set to 'true'")

    # Check if app-id is provided
    app_id = annotations.get('dapr.io/app-id')
    if app_id:
        # Validate app-id format (alphanumeric, hyphens, underscores)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', app_id):
            issues.append(f"Invalid app-id format: {app_id}. Only alphanumeric, hyphens, and underscores are allowed.")

    # If app-port is specified, validate it
    app_port = annotations.get('dapr.io/app-port')
    if app_port:
        try:
            port_num = int(app_port)
            if port_num < 1 or port_num > 65535:
                issues.append(f"Invalid port number: {app_port}. Must be between 1 and 65535.")
        except ValueError:
            issues.append(f"Invalid port number: {app_port}. Must be numeric.")

    return len(issues) == 0, issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_dapr_config.py <component_file.yaml> [sidecar_annotations_file.yaml]")
        print("Example: python validate_dapr_config.py kafka-component.yaml")
        sys.exit(1)

    component_file = sys.argv[1]

    try:
        with open(component_file, 'r') as f:
            if component_file.endswith('.json'):
                component_data = json.load(f)
            else:
                component_data = yaml.safe_load(f)

        if isinstance(component_data, list):
            # Handle multiple components in a single file
            for i, comp in enumerate(component_data):
                print(f"Validating component {i+1}: {comp.get('metadata', {}).get('name', 'unnamed')}")
                is_valid, error_msg = validate_dapr_component(comp)

                if is_valid:
                    print("✓ Component is valid")
                else:
                    print(f"✗ Component validation failed: {error_msg}")
        else:
            # Handle single component
            is_valid, error_msg = validate_dapr_component(component_data)

            if is_valid:
                print("✓ Component is valid")
                sys.exit(0)
            else:
                print(f"✗ Component validation failed: {error_msg}")
                sys.exit(1)

        # Check for sidecar annotations if provided
        if len(sys.argv) > 2:
            annotations_file = sys.argv[2]
            with open(annotations_file, 'r') as f:
                deployment_data = yaml.safe_load(f)

                # Extract annotations from the deployment template
                annotations = deployment_data.get('spec', {}).get('template', {}).get('metadata', {}).get('annotations', {})

                is_valid, issues = validate_dapr_sidecar_annotations(annotations)

                if is_valid:
                    print("✓ Sidecar annotations are valid")
                else:
                    print("✗ Sidecar annotations have issues:")
                    for issue in issues:
                        print(f"  - {issue}")

    except FileNotFoundError:
        print(f"Error: File {component_file} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()