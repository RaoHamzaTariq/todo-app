#!/bin/bash
# validate-k8s-manifests.sh
# Script to validate Kubernetes manifests before deployment

set -e

echo "Validating Kubernetes manifests..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Check if kubeval is installed (for schema validation)
if ! command -v kubeval &> /dev/null; then
    echo "Warning: kubeval is not installed - skipping schema validation"
    HAS_KUBEVAL=false
else
    HAS_KUBEVAL=true
fi

MANIFEST_DIR="${1:-.}"
echo "Validating manifests in: $MANIFEST_DIR"

# Find all YAML files
YAML_FILES=$(find "$MANIFEST_DIR" -name "*.yaml" -o -name "*.yml" | grep -v "values.yaml")

for file in $YAML_FILES; do
    echo "Validating: $file"

    # Basic syntax validation
    if ! yq eval . "$file" &>/dev/null; then
        echo "❌ Syntax error in $file"
        exit 1
    fi

    # Schema validation if kubeval is available
    if [ "$HAS_KUBEVAL" = true ]; then
        if ! kubeval -f "$file"; then
            echo "❌ Schema validation failed for $file"
            exit 1
        fi
    fi

    # Dry-run validation with kubectl
    if ! kubectl apply --dry-run=client -f "$file" &>/dev/null; then
        echo "❌ Dry-run validation failed for $file"
        exit 1
    fi

    echo "✅ Validated: $file"
done

echo "All manifests validated successfully!"