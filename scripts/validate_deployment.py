#!/usr/bin/env python3
"""
Deployment validation script for Places2Go.

This script validates that all deployment infrastructure is correctly configured
before attempting to deploy to Azure Static Web Apps.

Usage:
    python scripts/validate_deployment.py
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

import yaml


def check_file_exists(filepath: Path) -> Tuple[bool, str]:
    """Check if a file exists."""
    if filepath.exists():
        return True, f"✓ {filepath} exists"
    return False, f"✗ {filepath} is missing"


def validate_yaml(filepath: Path) -> Tuple[bool, str]:
    """Validate YAML file syntax."""
    try:
        with open(filepath) as f:
            yaml.safe_load(f)
        return True, f"✓ {filepath} is valid YAML"
    except Exception as e:
        return False, f"✗ {filepath} YAML error: {e}"


def validate_json(filepath: Path) -> Tuple[bool, str]:
    """Validate JSON file syntax."""
    try:
        with open(filepath) as f:
            json.load(f)
        return True, f"✓ {filepath} is valid JSON"
    except Exception as e:
        return False, f"✗ {filepath} JSON error: {e}"


def check_workflow_configuration(filepath: Path) -> List[Tuple[bool, str]]:
    """Check GitHub Actions workflow configuration."""
    results = []

    try:
        with open(filepath) as f:
            workflow = yaml.safe_load(f)

        # Check workflow name
        if "name" in workflow:
            results.append((True, "✓ Workflow has name"))
        else:
            results.append((False, "✗ Workflow missing name"))

        # Check triggers (YAML can use True/False/on/off as keys)
        has_triggers = "on" in workflow or True in workflow
        if has_triggers:
            results.append((True, "✓ Workflow has triggers"))
        else:
            results.append((False, "✗ Workflow missing triggers"))

        # Check jobs
        if "jobs" in workflow:
            results.append((True, "✓ Workflow has jobs"))
            jobs = workflow["jobs"]

            # Check for deploy job
            if any("deploy" in job_name.lower() for job_name in jobs.keys()):
                results.append((True, "✓ Workflow has deployment job"))
            else:
                results.append((False, "✗ Workflow missing deployment job"))

            # Check for test job
            if any("test" in job_name.lower() for job_name in jobs.keys()):
                results.append((True, "✓ Workflow has test job"))
            else:
                results.append((False, "⚠ Workflow missing test job (optional)"))

        else:
            results.append((False, "✗ Workflow missing jobs"))

    except Exception as e:
        results.append((False, f"✗ Error parsing workflow: {e}"))

    return results


def check_azure_config(filepath: Path) -> List[Tuple[bool, str]]:
    """Check Azure Static Web Apps configuration."""
    results = []

    try:
        with open(filepath) as f:
            config = json.load(f)

        # Check routes
        if "routes" in config:
            results.append((True, "✓ Azure config has routes"))
        else:
            results.append((False, "⚠ Azure config missing routes (optional)"))

        # Check global headers
        if "globalHeaders" in config:
            results.append((True, "✓ Azure config has security headers"))
            headers = config["globalHeaders"]

            # Check CSP
            if "content-security-policy" in headers:
                results.append((True, "✓ Content Security Policy configured"))
            else:
                results.append((False, "⚠ CSP not configured (recommended)"))
        else:
            results.append((False, "⚠ Global headers not configured (recommended)"))

    except Exception as e:
        results.append((False, f"✗ Error parsing Azure config: {e}"))

    return results


def main() -> int:
    """Run deployment validation checks."""
    print("=" * 60)
    print("Places2Go Deployment Validation")
    print("=" * 60)
    print()

    project_root = Path(__file__).resolve().parents[1]
    all_checks_passed = True

    # File existence checks
    print("📁 File Existence Checks")
    print("-" * 60)

    files_to_check = [
        project_root / ".github" / "workflows" / "deploy.yml",
        project_root / "staticwebapp.config.json",
        project_root / "deployment" / "index.html",
        project_root / "deployment" / "404.html",
        project_root / "config" / ".env.development",
        project_root / "config" / ".env.staging",
        project_root / "config" / ".env.production",
        project_root / "docs" / "DEPLOYMENT.md",
        project_root / "docs" / "ROLLBACK.md",
        project_root / "docs" / "MONITORING.md",
    ]

    for filepath in files_to_check:
        passed, message = check_file_exists(filepath)
        print(message)
        if not passed:
            all_checks_passed = False

    print()

    # YAML validation
    print("📋 YAML Validation")
    print("-" * 60)

    yaml_files = [
        project_root / ".github" / "workflows" / "deploy.yml",
    ]

    for filepath in yaml_files:
        if filepath.exists():
            passed, message = validate_yaml(filepath)
            print(message)
            if not passed:
                all_checks_passed = False
        else:
            print(f"⊘ Skipping {filepath} (doesn't exist)")

    print()

    # JSON validation
    print("📄 JSON Validation")
    print("-" * 60)

    json_files = [
        project_root / "staticwebapp.config.json",
    ]

    for filepath in json_files:
        if filepath.exists():
            passed, message = validate_json(filepath)
            print(message)
            if not passed:
                all_checks_passed = False
        else:
            print(f"⊘ Skipping {filepath} (doesn't exist)")

    print()

    # Workflow configuration checks
    print("⚙️  Workflow Configuration")
    print("-" * 60)

    workflow_file = project_root / ".github" / "workflows" / "deploy.yml"
    if workflow_file.exists():
        for passed, message in check_workflow_configuration(workflow_file):
            print(message)
            if not passed and message.startswith("✗"):
                all_checks_passed = False
    else:
        print("⊘ Skipping workflow checks (file doesn't exist)")

    print()

    # Azure configuration checks
    print("☁️  Azure Configuration")
    print("-" * 60)

    azure_config = project_root / "staticwebapp.config.json"
    if azure_config.exists():
        for passed, message in check_azure_config(azure_config):
            print(message)
            if not passed and message.startswith("✗"):
                all_checks_passed = False
    else:
        print("⊘ Skipping Azure checks (file doesn't exist)")

    print()

    # Build directory check
    print("🏗️  Build Configuration")
    print("-" * 60)

    build_dir = project_root / ".build" / "visualizations"
    if build_dir.exists():
        print(f"✓ Build directory exists: {build_dir}")

        # Check for visualization files
        viz_files = list(build_dir.glob("*.html"))
        if viz_files:
            print(f"✓ Found {len(viz_files)} visualization files")
        else:
            print("⚠ No visualization files found (run generators first)")
    else:
        print(f"⚠ Build directory doesn't exist: {build_dir}")
        print("  Run visualization generators to create it:")
        print("  python -m scripts.visualizations.destinations_map")

    print()

    # Deployment directory check
    print("📦 Deployment Assets")
    print("-" * 60)

    deployment_dir = project_root / "deployment"
    if deployment_dir.exists():
        print(f"✓ Deployment directory exists: {deployment_dir}")

        required_files = ["index.html", "404.html"]
        for filename in required_files:
            filepath = deployment_dir / filename
            if filepath.exists():
                print(f"✓ {filename} exists")
            else:
                print(f"✗ {filename} is missing")
                all_checks_passed = False
    else:
        print(f"✗ Deployment directory doesn't exist: {deployment_dir}")
        all_checks_passed = False

    print()

    # Summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ All validation checks passed!")
        print()
        print("Next steps:")
        print("1. Create Azure Static Web App resource")
        print("2. Add AZURE_STATIC_WEB_APPS_API_TOKEN to GitHub Secrets")
        print("3. Push to main branch to trigger deployment")
        print()
        print("See docs/DEPLOYMENT.md for detailed instructions")
        return 0
    else:
        print("❌ Some validation checks failed")
        print()
        print("Please fix the issues above before deploying.")
        print("See docs/DEPLOYMENT.md for help")
        return 1


if __name__ == "__main__":
    sys.exit(main())
