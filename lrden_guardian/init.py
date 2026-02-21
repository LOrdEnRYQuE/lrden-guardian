#!/usr/bin/env python3
"""
LRDEnE Guardian - Project Initialization Tool
==========================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Initialize LRDEnE Guardian in any project with configuration files,
templates, and setup automation.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

def create_parser() -> argparse.ArgumentParser:
    """Create initialization argument parser"""
    
    parser = argparse.ArgumentParser(
        prog="lrden-init",
        description="Initialize LRDEnE Guardian in your project",
        epilog="Copyright (c) 2026 LRDEnE. All rights reserved."
    )
    
    parser.add_argument(
        "--project-dir",
        type=str,
        default=".",
        help="Project directory (default: current directory)"
    )
    
    parser.add_argument(
        "--config-type",
        choices=["basic", "enterprise", "security", "custom"],
        default="basic",
        help="Configuration type (default: basic)"
    )
    
    parser.add_argument(
        "--license-key",
        type=str,
        help="LRDEnE Guardian license key"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing configuration"
    )
    
    parser.add_argument(
        "--production",
        action="store_true",
        help="Production-ready configuration"
    )
    
    return parser

def create_config_file(project_dir: Path, config_type: str, license_key: Optional[str] = None) -> None:
    """Create LRDEnE Guardian configuration file"""
    
    config_dir = project_dir / ".lrden"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "guardian_config.json"
    
    # Base configuration
    config = {
        "version": "1.0.0",
        "project_name": project_dir.name,
        "initialized_at": str(Path.cwd()),
        "license_key": license_key or None,
        "settings": {
            "confidence_threshold": 0.7,
            "risk_threshold": "medium",
            "enable_monitoring": True,
            "enable_analytics": True,
            "log_level": "INFO"
        },
        "validation_types": [
            "syntax",
            "semantics", 
            "factual",
            "context",
            "source",
            "risk_pattern",
            "security"
        ]
    }
    
    # Configuration type specific settings
    if config_type == "enterprise":
        config["settings"].update({
            "confidence_threshold": 0.8,
            "risk_threshold": "low",
            "enable_monitoring": True,
            "enable_analytics": True,
            "enable_compliance": True,
            "log_level": "DEBUG"
        })
        config["validation_types"].extend(["compliance", "performance"])
    
    elif config_type == "security":
        config["settings"].update({
            "confidence_threshold": 0.9,
            "risk_threshold": "low",
            "enable_monitoring": True,
            "enable_security_scanning": True,
            "enable_vulnerability_check": True,
            "log_level": "WARNING"
        })
        config["validation_types"].extend(["vulnerability", "compliance"])
    
    elif config_type == "production":
        config["settings"].update({
            "confidence_threshold": 0.85,
            "risk_threshold": "medium",
            "enable_monitoring": True,
            "enable_analytics": True,
            "enable_alerting": True,
            "enable_reporting": True,
            "log_level": "INFO"
        })
    
    # Write configuration
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created configuration: {config_file}")

def create_gitignore(project_dir: Path) -> None:
    """Create .gitignore for LRDEnE files"""
    
    gitignore_file = project_dir / ".gitignore"
    
    gitignore_content = """
# LRDEnE Guardian
.lrden/
guardian_logs/
guardian_reports/
guardian_cache/

# LRDEnE Guardian temporary files
*.guardian.tmp
.guardian_*.log

# LRDEnE Guardian analytics
guardian_analytics/
monitoring_data/
"""
    
    if not gitignore_file.exists():
        with open(gitignore_file, 'a') as f:
            f.write(gitignore_content)
        print(f"✅ Updated .gitignore")
    else:
        # Check if LRDEnE section already exists
        with open(gitignore_file, 'r') as f:
            content = f.read()
        
        if "# LRDEnE Guardian" not in content:
            with open(gitignore_file, 'a') as f:
                f.write(gitignore_content)
            print(f"✅ Updated .gitignore")
        else:
            print(f"ℹ️  .gitignore already contains LRDEnE entries")

def create_example_script(project_dir: Path) -> None:
    """Create example usage script"""
    
    example_file = project_dir / "guardian_example.py"
    
    example_content = '''#!/usr/bin/env python3
"""
LRDEnE Guardian - Example Usage
=============================

This example shows how to use LRDEnE Guardian in your project.
"""

from lrden_guardian import create_lrden_guardian

def main():
    """Example LRDEnE Guardian usage"""
    
    # Initialize LRDEnE Guardian
    guardian = create_lrden_guardian()
    
    # Example content to analyze
    content = """
    React is a JavaScript framework created by Google in 2015.
    It's the most popular frontend framework with 90% market share.
    React applications are completely immune to XSS attacks.
    
    According to studies, React is 10x faster than Vue and Angular.
    """
    
    # Analyze content
    print("🛡️ Analyzing content with LRDEnE Guardian...")
    result = guardian.analyze_content(content)
    
    # Display results
    print(f"✅ Content Safe: {'YES' if result.is_safe else 'NO'}")
    print(f"📊 Risk Level: {result.risk_level.value.upper()}")
    print(f"🔍 Confidence: {result.confidence_score:.2f}")
    print(f"⭐ Guardian Score: {result.guardian_score:.3f}")
    
    if not result.is_safe:
        print("\\n🚨 Issues Detected:")
        for issue in result.detected_issues[:5]:
            print(f"   • {issue}")
        
        print("\\n💡 Recommendations:")
        for rec in result.recommendations:
            print(f"   • {rec}")
    
    print("\\n🛡️ LRDEnE Guardian analysis complete!")

if __name__ == "__main__":
    main()
'''
    
    with open(example_file, 'w') as f:
        f.write(example_content)
    
    print(f"✅ Created example script: {example_file}")

def create_requirements(project_dir: Path) -> None:
    """Create requirements file"""
    
    requirements_file = project_dir / "requirements.txt"
    
    requirements_content = """
# LRDEnE Guardian
lrden-guardian>=1.0.0

# Optional dependencies for enhanced features
python-dateutil>=2.8.0
pydantic>=2.0.0
rich>=13.0.0
"""
    
    if not requirements_file.exists():
        with open(requirements_file, 'w') as f:
            f.write(requirements_content)
        print(f"✅ Created requirements.txt")
    else:
        # Check if LRDEnE already in requirements
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        if "lrden-guardian" not in content:
            with open(requirements_file, 'a') as f:
                f.write("\n# LRDEnE Guardian\nlrden-guardian>=1.0.0\n")
            print(f"✅ Updated requirements.txt")
        else:
            print(f"ℹ️  requirements.txt already contains LRDEnE Guardian")

def create_readme_section(project_dir: Path) -> None:
    """Add LRDEnE Guardian section to README"""
    
    readme_file = project_dir / "README.md"
    
    guardian_section = '''
## 🛡️ LRDEnE Guardian Integration

This project uses LRDEnE Guardian for AI safety and hallucination detection.

### Installation

```bash
pip install lrden-guardian
```

### Usage

```python
from lrden_guardian import create_lrden_guardian

guardian = create_lrden_guardian()
result = guardian.analyze_content(content)

if result.is_safe:
    print("✅ Content is safe")
else:
    print(f"🚨 Risk detected: {result.risk_level.value}")
```

### Configuration

LRDEnE Guardian is configured via `.lrden/guardian_config.json`.

For more information, see [LRDEnE Guardian Documentation](https://github.com/LRDEnE/lrden-guardian).
'''
    
    if not readme_file.exists():
        # Create new README
        with open(readme_file, 'w') as f:
            f.write(f"# {project_dir.name}\n\n")
            f.write(guardian_section)
        print(f"✅ Created README.md with LRDEnE Guardian section")
    else:
        # Check if LRDEnE section already exists
        with open(readme_file, 'r') as f:
            content = f.read()
        
        if "LRDEnE Guardian Integration" not in content:
            with open(readme_file, 'a') as f:
                f.write(f"\n{guardian_section}")
            print(f"✅ Added LRDEnE Guardian section to README.md")
        else:
            print(f"ℹ️  README.md already contains LRDEnE Guardian section")

def initialize_project(project_dir: str, config_type: str, license_key: Optional[str] = None, force: bool = False) -> None:
    """Initialize LRDEnE Guardian in project"""
    
    project_path = Path(project_dir).resolve()
    
    if not project_path.exists():
        print(f"❌ Project directory '{project_dir}' does not exist")
        sys.exit(1)
    
    print(f"🛡️ Initializing LRDEnE Guardian in: {project_path}")
    
    # Check if already initialized
    config_dir = project_path / ".lrden"
    if config_dir.exists() and not force:
        print(f"❌ LRDEnE Guardian already initialized in this project")
        print(f"   Use --force to overwrite existing configuration")
        sys.exit(1)
    
    # Create configuration
    create_config_file(project_path, config_type, license_key)
    
    # Create supporting files
    create_gitignore(project_path)
    create_example_script(project_path)
    create_requirements(project_path)
    create_readme_section(project_path)
    
    # Create directories
    (project_path / "guardian_logs").mkdir(exist_ok=True)
    (project_path / "guardian_reports").mkdir(exist_ok=True)
    
    print(f"\n🎉 LRDEnE Guardian initialized successfully!")
    print(f"📁 Configuration directory: {config_dir}")
    print(f"📖 Example script: guardian_example.py")
    print(f"⚙️  Configuration type: {config_type}")
    
    if license_key:
        print(f"🔑 License key configured")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Install dependencies: pip install -r requirements.txt")
    print(f"   2. Run example: python guardian_example.py")
    print(f"   3. Configure settings in .lrden/guardian_config.json")
    print(f"   4. Integrate into your application")

def main() -> None:
    """Main initialization entry point"""
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Determine config type
    config_type = args.config_type
    if args.production:
        config_type = "production"
    
    print("🛡️ LRDEnE Guardian Project Initialization")
    print("=" * 40)
    
    try:
        initialize_project(
            project_dir=args.project_dir,
            config_type=config_type,
            license_key=args.license_key,
            force=args.force
        )
    
    except KeyboardInterrupt:
        print("\n🛡️ Initialization interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
