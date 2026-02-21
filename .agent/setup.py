#!/usr/bin/env python3
"""
Enhanced VS Code Agent System Setup Script
==========================================

Automated setup and installation script for the enhanced VS Code agent system.
Handles dependency installation, configuration, and system validation.

Usage:
    python setup.py [--dev] [--force] [--no-tests]
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any
import platform

class SetupManager:
    """Manages the setup and installation process"""
    
    def __init__(self, agent_root: Path, dev_mode: bool = False, force: bool = False, skip_tests: bool = False):
        self.agent_root = agent_root
        self.dev_mode = dev_mode
        self.force = force
        self.skip_tests = skip_tests
        
        self.core_dir = agent_root / "core"
        self.config_dir = agent_root / "config"
        self.logs_dir = agent_root / "logs"
        
        # Required packages
        self.base_packages = [
            "pyyaml>=6.0",
            "psutil>=5.9.0",
            "requests>=2.28.0"
        ]
        
        self.dev_packages = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0"
        ]
        
        self.setup_steps = [
            ("Checking Python version", self._check_python_version),
            ("Creating directories", self._create_directories),
            ("Installing dependencies", self._install_dependencies),
            ("Setting up configuration", self._setup_configuration),
            ("Validating installation", self._validate_installation),
            ("Running system tests", self._run_system_tests)
        ]
    
    def run_setup(self) -> bool:
        """Run the complete setup process"""
        print("🚀 Enhanced VS Code Agent System Setup")
        print("=" * 50)
        
        try:
            for step_name, step_func in self.setup_steps:
                if step_name == "Running system tests" and self.skip_tests:
                    print(f"⏭️  Skipping: {step_name}")
                    continue
                
                print(f"🔧 {step_name}...")
                success = step_func()
                
                if not success:
                    print(f"❌ Failed: {step_name}")
                    return False
                
                print(f"✅ Completed: {step_name}")
            
            print("\n🎉 Setup completed successfully!")
            self._print_next_steps()
            return True
            
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            return False
    
    def _check_python_version(self) -> bool:
        """Check Python version compatibility"""
        version = sys.version_info
        required_version = (3, 8)
        
        if version < required_version:
            print(f"❌ Python {version.major}.{version.minor} detected. Python {required_version[0]}.{required_version[1]}+ required.")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def _create_directories(self) -> bool:
        """Create necessary directories"""
        directories = [
            self.agent_root,
            self.core_dir,
            self.config_dir,
            self.logs_dir,
            self.agent_root / "skills",
            self.agent_root / "agents",
            self.agent_root / "workflows",
            self.agent_root / "scripts",
            self.agent_root / "rules"
        ]
        
        for directory in directories:
            try:
                directory.mkdir(exist_ok=True, parents=True)
                print(f"  📁 Created: {directory}")
            except Exception as e:
                print(f"  ❌ Failed to create {directory}: {e}")
                return False
        
        return True
    
    def _install_dependencies(self) -> bool:
        """Install required Python packages"""
        packages = self.base_packages.copy()
        
        if self.dev_mode:
            packages.extend(self.dev_packages)
        
        for package in packages:
            try:
                print(f"  📦 Installing {package}...")
                
                # Use pip to install package
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"  ❌ Failed to install {package}: {result.stderr}")
                    return False
                
                print(f"  ✅ Installed {package}")
                
            except Exception as e:
                print(f"  ❌ Error installing {package}: {e}")
                return False
        
        return True
    
    def _setup_configuration(self) -> bool:
        """Setup initial configuration"""
        try:
            # Create default configuration
            config = {
                "ide_detection": {
                    "auto_detect": True,
                    "fallback_agent": "orchestrator"
                },
                "skill_discovery": {
                    "auto_discover": True,
                    "cache_results": True,
                    "validate_skills": True
                },
                "ai_routing": {
                    "auto_route": True,
                    "confidence_threshold": 0.7,
                    "max_secondary_agents": 3
                },
                "performance": {
                    "cache_size": 100,
                    "parallel_processing": True,
                    "optimize_for_speed": True
                },
                "security": {
                    "encrypt_api_keys": True,
                    "validate_inputs": True,
                    "audit_logging": True
                },
                "logging": {
                    "level": "INFO",
                    "file_logging": True,
                    "console_logging": True
                },
                "integration": {
                    "mcp_servers": {},
                    "extensions": {},
                    "external_apis": {}
                }
            }
            
            # Save configuration
            config_file = self.config_dir / "global.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"  📄 Created configuration: {config_file}")
            
            # Create MCP configuration
            mcp_config = {
                "mcpServers": {
                    "filesystem": {
                        "command": "python",
                        "args": ["-m", "mcp_filesystem"],
                        "capabilities": ["file_system"],
                        "config": {"allowed_directories": [str(self.agent_root.parent)]}
                    },
                    "database": {
                        "command": "python",
                        "args": ["-m", "mcp_database"],
                        "capabilities": ["database"],
                        "config": {"database_url": "sqlite:///agent.db"}
                    }
                }
            }
            
            mcp_config_file = self.config_dir / "mcp_config.json"
            with open(mcp_config_file, 'w') as f:
                json.dump(mcp_config, f, indent=2)
            
            print(f"  📄 Created MCP configuration: {mcp_config_file}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Configuration setup failed: {e}")
            return False
    
    def _validate_installation(self) -> bool:
        """Validate the installation"""
        try:
            # Import core modules to check they work
            sys.path.insert(0, str(self.core_dir))
            
            # Test IDE detector
            from ide_detector import IDEDetector
            detector = IDEDetector()
            print(f"  🔍 IDE detected: {detector.ide_info.name}")
            
            # Test skill discovery
            from skill_discovery import SkillDiscovery
            discovery = SkillDiscovery(self.agent_root)
            skills = discovery.discover_all_skills()
            print(f"  🛠️ Skills discovered: {len(skills)}")
            
            # Test AI router
            from ai_router import AIRouter
            router = AIRouter(self.agent_root)
            print(f"  🤖 Agents loaded: {len(router.agent_profiles)}")
            
            # Test configuration manager
            from config_manager import ConfigManager
            config_manager = ConfigManager(self.agent_root)
            validation = config_manager.validate_configuration()
            print(f"  ⚙️ Configuration valid: {validation['valid']}")
            
            # Test MCP integration
            from mcp_integration import MCPIntegration
            mcp_integration = MCPIntegration(self.agent_root)
            summary = mcp_integration.get_integration_summary()
            print(f"  🔌 MCP servers: {summary['total_servers']}")
            
            return True
            
        except ImportError as e:
            print(f"  ❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Validation error: {e}")
            return False
    
    def _run_system_tests(self) -> bool:
        """Run system tests to validate installation"""
        try:
            sys.path.insert(0, str(self.core_dir))
            
            from test_framework import TestFramework, TestType
            
            # Create test framework
            test_framework = TestFramework(self.agent_root)
            
            # Run health checks
            print("  🏥 Running health checks...")
            health_results = test_framework.run_all_tests([TestType.HEALTH])
            
            if health_results.failed_count > 0 or health_results.error_count > 0:
                print(f"  ⚠️ Health issues found: {health_results.failed_count + health_results.error_count}")
                
                # Show details
                for test in health_results.tests:
                    if test.status.value in ["failed", "error"]:
                        print(f"    ❌ {test.name}: {test.message}")
                
                if not self.force:
                    return False
            
            print(f"  ✅ Health checks passed: {health_results.passed_count}/{len(health_results.tests)}")
            
            # Run core component tests
            print("  🧪 Running component tests...")
            component_results = test_framework.run_all_tests([TestType.UNIT])
            
            if component_results.failed_count > 0 or component_results.error_count > 0:
                print(f"  ⚠️ Component test issues: {component_results.failed_count + component_results.error_count}")
                
                if not self.force:
                    return False
            
            print(f"  ✅ Component tests passed: {component_results.passed_count}/{len(component_results.tests)}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Test execution failed: {e}")
            return not self.force  # Continue if force mode
    
    def _print_next_steps(self):
        """Print next steps for the user"""
        print("\n📋 Next Steps:")
        print("1. Start the system:")
        print(f"   cd {self.agent_root}")
        print("   python core/orchestrator.py")
        print()
        print("2. Test with a sample request:")
        print("   python -c \"from core.orchestrator import EnhancedOrchestrator; from pathlib import Path; o = EnhancedOrchestrator(Path.cwd() / '.agent'); print(o.process_request('Create a React component'))\"")
        print()
        print("3. View system status:")
        print("   python -c \"from core.orchestrator import EnhancedOrchestrator; from pathlib import Path; import json; o = EnhancedOrchestrator(Path.cwd() / '.agent'); print(json.dumps(o.get_system_status(), indent=2))\"")
        print()
        print("4. Read the documentation:")
        print(f"   cat {self.agent_root / 'README.md'}")
        print()
        print("🎉 Your Enhanced VS Code Agent System is ready!")

def main():
    """Main setup entry point"""
    parser = argparse.ArgumentParser(description="Setup Enhanced VS Code Agent System")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    parser.add_argument("--force", action="store_true", help="Force setup despite warnings")
    parser.add_argument("--no-tests", action="store_true", help="Skip system tests")
    parser.add_argument("--agent-root", type=str, help="Custom agent root directory")
    
    args = parser.parse_args()
    
    # Determine agent root
    if args.agent_root:
        agent_root = Path(args.agent_root)
    else:
        # Default to current directory's .agent folder
        agent_root = Path.cwd() / ".agent"
    
    # Create setup manager
    setup_manager = SetupManager(
        agent_root=agent_root,
        dev_mode=args.dev,
        force=args.force,
        skip_tests=args.no_tests
    )
    
    # Run setup
    success = setup_manager.run_setup()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
