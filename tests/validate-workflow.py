#!/usr/bin/env python3
"""
GitHub Actions Workflow JSON Schema Validator
Validates the docker-build.yml workflow against GitHub Actions schema
"""

import json
import yaml
import sys
import os
from pathlib import Path

def load_workflow_schema():
    """GitHub Actions Workflow Schema (simplified)"""
    return {
        "type": "object",
        "required": ["name", "on", "jobs"],
        "properties": {
            "name": {"type": "string"},
            "on": {
                "type": "object",
                "properties": {
                    "push": {"type": "object"},
                    "workflow_dispatch": {"type": "object"}
                }
            },
            "env": {"type": "object"},
            "jobs": {
                "type": "object",
                "patternProperties": {
                    "^[a-zA-Z_][a-zA-Z0-9_-]*$": {
                        "type": "object",
                        "required": ["runs-on", "steps"],
                        "properties": {
                            "runs-on": {"type": "string"},
                            "permissions": {"type": "object"},
                            "steps": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "uses": {"type": "string"},
                                        "with": {"type": "object"},
                                        "run": {"type": "string"},
                                        "if": {"type": "string"},
                                        "id": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

def validate_workflow_file(workflow_path):
    """Validate workflow file against schema"""
    try:
        with open(workflow_path, 'r') as f:
            workflow_data = yaml.safe_load(f)
        
        # Basic structure validation
        schema = load_workflow_schema()
        errors = []
        
        # Check required top-level keys
        for required_key in schema["required"]:
            if required_key not in workflow_data:
                errors.append(f"Missing required key: {required_key}")
        
        # Validate jobs structure
        if "jobs" in workflow_data:
            for job_name, job_data in workflow_data["jobs"].items():
                if not isinstance(job_data, dict):
                    errors.append(f"Job '{job_name}' must be an object")
                    continue
                
                # Check required job keys
                for required_job_key in ["runs-on", "steps"]:
                    if required_job_key not in job_data:
                        errors.append(f"Job '{job_name}' missing required key: {required_job_key}")
                
                # Validate steps
                if "steps" in job_data:
                    if not isinstance(job_data["steps"], list):
                        errors.append(f"Job '{job_name}' steps must be an array")
                    else:
                        for i, step in enumerate(job_data["steps"]):
                            if not isinstance(step, dict):
                                errors.append(f"Job '{job_name}' step {i} must be an object")
        
        return errors
        
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    except FileNotFoundError:
        return [f"Workflow file not found: {workflow_path}"]
    except Exception as e:
        return [f"Validation error: {e}"]

def validate_buildkit_features(workflow_path):
    """Validate BuildKit-specific features"""
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        buildkit_checks = [
            ("docker/setup-buildx-action", "Missing Docker Buildx setup"),
            ("target:", "Missing multi-stage build targets"),
            ("cache-from:", "Missing cache-from configuration"),
            ("cache-to:", "Missing cache-to configuration"),
            ("type=gha", "Missing GitHub Actions cache"),
            ("platforms:", "Missing multi-platform configuration"),
            ("linux/amd64,linux/arm64", "Missing AMD64/ARM64 platforms")
        ]
        
        errors = []
        for check, error_msg in buildkit_checks:
            if check not in content:
                errors.append(error_msg)
        
        return errors
        
    except Exception as e:
        return [f"BuildKit validation error: {e}"]

def main():
    """Main validation function"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    workflow_file = project_root / ".github" / "workflows" / "docker-build.yml"
    
    print("🔍 Validating GitHub Actions Workflow...")
    print(f"📄 File: {workflow_file}")
    print()
    
    # Schema validation
    schema_errors = validate_workflow_file(workflow_file)
    if schema_errors:
        print("❌ Schema Validation Errors:")
        for error in schema_errors:
            print(f"  • {error}")
    else:
        print("✅ Schema validation passed")
    
    print()
    
    # BuildKit validation
    buildkit_errors = validate_buildkit_features(workflow_file)
    if buildkit_errors:
        print("❌ BuildKit Validation Errors:")
        for error in buildkit_errors:
            print(f"  • {error}")
    else:
        print("✅ BuildKit validation passed")
    
    print()
    
    # Summary
    total_errors = len(schema_errors) + len(buildkit_errors)
    if total_errors == 0:
        print("🎉 All validations passed!")
        return 0
    else:
        print(f"💥 Found {total_errors} validation error(s)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
