#!/usr/bin/env python3
"""
Enhanced Configuration System - Enhanced VS Code Agent System
============================================================

Advanced configuration management with IDE detection, dynamic settings,
and intelligent adaptation. Supports multiple IDEs and environments.

Features:
- Universal IDE configuration
- Dynamic setting management
- Environment adaptation
- Configuration validation
- Profile management
- Settings synchronization
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import shutil

from ide_detector import IDEDetector, IDEType

class ConfigScope(Enum):
    GLOBAL = "global"
    WORKSPACE = "workspace"
    PROJECT = "project"
    USER = "user"

class ConfigFormat(Enum):
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"

@dataclass
class ConfigProfile:
    """Configuration profile for different environments"""
    name: str
    scope: ConfigScope
    settings: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    active: bool = False
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['scope'] = self.scope.value
        return data

@dataclass
class SystemConfig:
    """System-wide configuration"""
    ide_detection: Dict[str, Any] = field(default_factory=dict)
    skill_discovery: Dict[str, Any] = field(default_factory=dict)
    ai_routing: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    security: Dict[str, Any] = field(default_factory=dict)
    logging: Dict[str, Any] = field(default_factory=dict)
    integration: Dict[str, Any] = field(default_factory=dict)

class ConfigManager:
    """Enhanced configuration management system"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.config_dir = agent_root / "config"
        self.core_dir = agent_root / "core"
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize IDE detector
        self.ide_detector = IDEDetector()
        
        # Configuration file paths
        self.global_config_path = self.config_dir / "global.json"
        self.workspace_config_path = self.config_dir / "workspace.json"
        self.project_config_path = self.agent_root / "project.json"
        self.user_config_path = self.config_dir / "user.json"
        
        # Profile storage
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Current configuration
        self.system_config = SystemConfig()
        self.profiles: Dict[str, ConfigProfile] = {}
        
        # Load configurations
        self._load_configurations()
        self._load_profiles()
    
    def _load_configurations(self):
        """Load all configuration files"""
        
        # Load global configuration
        if self.global_config_path.exists():
            try:
                with open(self.global_config_path, 'r') as f:
                    global_config = json.load(f)
                self._update_system_config(global_config, "global")
            except Exception as e:
                print(f"Error loading global config: {e}")
        
        # Load workspace configuration
        if self.workspace_config_path.exists():
            try:
                with open(self.workspace_config_path, 'r') as f:
                    workspace_config = json.load(f)
                self._update_system_config(workspace_config, "workspace")
            except Exception as e:
                print(f"Error loading workspace config: {e}")
        
        # Load project configuration
        if self.project_config_path.exists():
            try:
                with open(self.project_config_path, 'r') as f:
                    project_config = json.load(f)
                self._update_system_config(project_config, "project")
            except Exception as e:
                print(f"Error loading project config: {e}")
        
        # Load user configuration
        if self.user_config_path.exists():
            try:
                with open(self.user_config_path, 'r') as f:
                    user_config = json.load(f)
                self._update_system_config(user_config, "user")
            except Exception as e:
                print(f"Error loading user config: {e}")
        
        # Apply IDE-specific defaults
        self._apply_ide_defaults()
    
    def _update_system_config(self, config: Dict[str, Any], scope: str):
        """Update system configuration with loaded config"""
        for key, value in config.items():
            if hasattr(self.system_config, key):
                current_value = getattr(self.system_config, key)
                if isinstance(current_value, dict):
                    current_value.update(value)
                else:
                    setattr(self.system_config, key, value)
    
    def _apply_ide_defaults(self):
        """Apply IDE-specific default configurations"""
        ide_info = self.ide_detector.ide_info
        
        # IDE-specific settings
        ide_defaults = {
            IDEType.VSCODE: {
                "file_operations": "standard",
                "command_palette": "vscode",
                "extension_api": "vscode"
            },
            IDEType.WINDSURF: {
                "file_operations": "enhanced",
                "command_palette": "windsurf",
                "extension_api": "vscode-compatible",
                "ai_features": "native"
            },
            IDEType.CURSOR: {
                "file_operations": "ai-enhanced",
                "command_palette": "cursor",
                "extension_api": "vscode-compatible",
                "ai_features": "integrated"
            }
        }
        
        defaults = ide_defaults.get(ide_info.type, {})
        
        # Update integration settings
        if defaults:
            self.system_config.integration.update({
                "ide_type": ide_info.type.value,
                "ide_name": ide_info.name,
                "platform": ide_info.platform,
                **defaults
            })
    
    def _load_profiles(self):
        """Load configuration profiles"""
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile_data = json.load(f)
                
                profile = ConfigProfile(
                    name=profile_data["name"],
                    scope=ConfigScope(profile_data["scope"]),
                    settings=profile_data["settings"],
                    created_at=datetime.fromisoformat(profile_data["created_at"]),
                    updated_at=datetime.fromisoformat(profile_data["updated_at"]),
                    active=profile_data.get("active", False),
                    description=profile_data.get("description", "")
                )
                
                self.profiles[profile.name] = profile
                
            except Exception as e:
                print(f"Error loading profile {profile_file}: {e}")
    
    def create_profile(self, name: str, scope: ConfigScope, settings: Dict[str, Any], description: str = "") -> ConfigProfile:
        """Create a new configuration profile"""
        
        # Check if profile already exists
        if name in self.profiles:
            raise ValueError(f"Profile '{name}' already exists")
        
        profile = ConfigProfile(
            name=name,
            scope=scope,
            settings=settings,
            description=description
        )
        
        # Save profile
        self._save_profile(profile)
        self.profiles[name] = profile
        
        return profile
    
    def _save_profile(self, profile: ConfigProfile):
        """Save profile to file"""
        profile_file = self.profiles_dir / f"{profile.name}.json"
        
        with open(profile_file, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
    
    def activate_profile(self, name: str):
        """Activate a configuration profile"""
        if name not in self.profiles:
            raise ValueError(f"Profile '{name}' not found")
        
        # Deactivate all profiles in the same scope
        scope = self.profiles[name].scope
        for profile in self.profiles.values():
            if profile.scope == scope:
                profile.active = False
                self._save_profile(profile)
        
        # Activate the requested profile
        self.profiles[name].active = True
        self.profiles[name].updated_at = datetime.now()
        self._save_profile(self.profiles[name])
        
        # Apply profile settings
        self._apply_profile_settings(self.profiles[name])
    
    def _apply_profile_settings(self, profile: ConfigProfile):
        """Apply profile settings to system configuration"""
        for key, value in profile.settings.items():
            if hasattr(self.system_config, key):
                current_value = getattr(self.system_config, key)
                if isinstance(current_value, dict):
                    current_value.update(value)
                else:
                    setattr(self.system_config, key, value)
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting value"""
        
        # Navigate through nested keys
        keys = key.split('.')
        value = self.system_config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_setting(self, key: str, value: Any, scope: ConfigScope = ConfigScope.PROJECT):
        """Set a configuration setting value"""
        
        # Navigate through nested keys
        keys = key.split('.')
        config_dict = {}
        
        # Build nested dictionary
        current = config_dict
        for k in keys[:-1]:
            current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        
        # Update system configuration
        self._update_system_config(config_dict, scope.value)
        
        # Save to appropriate config file
        self._save_scope_config(scope)
    
    def _save_scope_config(self, scope: ConfigScope):
        """Save configuration for specific scope"""
        config_data = {
            "ide_detection": self.system_config.ide_detection,
            "skill_discovery": self.system_config.skill_discovery,
            "ai_routing": self.system_config.ai_routing,
            "performance": self.system_config.performance,
            "security": self.system_config.security,
            "logging": self.system_config.logging,
            "integration": self.system_config.integration
        }
        
        # Determine file path based on scope
        if scope == ConfigScope.GLOBAL:
            config_path = self.global_config_path
        elif scope == ConfigScope.WORKSPACE:
            config_path = self.workspace_config_path
        elif scope == ConfigScope.PROJECT:
            config_path = self.project_config_path
        elif scope == ConfigScope.USER:
            config_path = self.user_config_path
        else:
            return
        
        # Save configuration
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration"""
        issues = []
        warnings = []
        
        # Validate IDE detection
        if not self.system_config.ide_detection:
            issues.append("IDE detection configuration is missing")
        
        # Validate skill discovery
        skill_config = self.system_config.skill_discovery
        if not skill_config.get("skills_directory"):
            warnings.append("Skills directory not configured")
        
        # Validate AI routing
        routing_config = self.system_config.ai_routing
        if not routing_config.get("max_confidence_threshold"):
            warnings.append("AI routing confidence threshold not set")
        
        # Validate performance settings
        perf_config = self.system_config.performance
        if perf_config.get("cache_size", 0) > 1000:
            warnings.append("Cache size is very large, may impact performance")
        
        # Validate security settings
        security_config = self.system_config.security
        if not security_config.get("api_key_encrypted"):
            warnings.append("API keys should be encrypted")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "health_score": max(0, 100 - len(issues) * 20 - len(warnings) * 5)
        }
    
    def optimize_configuration(self) -> Dict[str, Any]:
        """Optimize configuration for current environment"""
        optimizations = []
        
        # IDE-specific optimizations
        ide_info = self.ide_detector.ide_info
        
        if ide_info.type == IDEType.WINDSURF:
            # Windsurf optimizations
            self.system_config.performance.update({
                "parallel_processing": True,
                "ai_acceleration": True,
                "cache_ai_responses": True
            })
            optimizations.append("Enabled Windsurf AI acceleration")
        
        elif ide_info.type == IDEType.VSCODE:
            # VS Code optimizations
            self.system_config.performance.update({
                "extension_compatibility": True,
                "standard_api": True
            })
            optimizations.append("Optimized for VS Code extensions")
        
        # Platform-specific optimizations
        if ide_info.platform == "Darwin":  # macOS
            self.system_config.performance.update({
                "file_system_watcher": True,
                "spotlight_integration": True
            })
            optimizations.append("Enabled macOS optimizations")
        
        elif ide_info.platform == "Windows":
            self.system_config.performance.update({
                "windows_path_handling": True,
                "powershell_integration": True
            })
            optimizations.append("Enabled Windows optimizations")
        
        # Performance optimizations
        current_config = self.system_config.performance
        
        # Auto-tune cache size based on available memory
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        if memory_gb > 16:
            current_config["cache_size"] = 500
            optimizations.append("Increased cache size for high-memory system")
        elif memory_gb > 8:
            current_config["cache_size"] = 200
            optimizations.append("Set moderate cache size")
        else:
            current_config["cache_size"] = 50
            optimizations.append("Reduced cache size for low-memory system")
        
        # Save optimized configuration
        self._save_scope_config(ConfigScope.PROJECT)
        
        return {
            "optimizations": optimizations,
            "performance_settings": current_config,
            "ide_type": ide_info.type.value,
            "platform": ide_info.platform
        }
    
    def export_configuration(self, export_path: Path, format: ConfigFormat = ConfigFormat.JSON) -> bool:
        """Export current configuration to file"""
        try:
            config_data = {
                "exported_at": datetime.now().isoformat(),
                "ide_info": self.ide_detector.to_dict(),
                "system_config": {
                    "ide_detection": self.system_config.ide_detection,
                    "skill_discovery": self.system_config.skill_discovery,
                    "ai_routing": self.system_config.ai_routing,
                    "performance": self.system_config.performance,
                    "security": self.system_config.security,
                    "logging": self.system_config.logging,
                    "integration": self.system_config.integration
                },
                "profiles": {name: profile.to_dict() for name, profile in self.profiles.items()}
            }
            
            if format == ConfigFormat.JSON:
                with open(export_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
            elif format == ConfigFormat.YAML:
                with open(export_path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return True
            
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return False
    
    def import_configuration(self, import_path: Path, merge: bool = True) -> bool:
        """Import configuration from file"""
        try:
            with open(import_path, 'r') as f:
                if import_path.suffix.lower() == '.yaml' or import_path.suffix.lower() == '.yml':
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            if not merge:
                # Replace entire configuration
                self.system_config = SystemConfig()
                self.profiles = {}
            
            # Import system configuration
            if "system_config" in config_data:
                self._update_system_config(config_data["system_config"], "imported")
            
            # Import profiles
            if "profiles" in config_data:
                for profile_data in config_data["profiles"].values():
                    profile = ConfigProfile(
                        name=profile_data["name"],
                        scope=ConfigScope(profile_data["scope"]),
                        settings=profile_data["settings"],
                        created_at=datetime.fromisoformat(profile_data["created_at"]),
                        updated_at=datetime.fromisoformat(profile_data["updated_at"]),
                        active=profile_data.get("active", False),
                        description=profile_data.get("description", "")
                    )
                    self.profiles[profile.name] = profile
                    self._save_profile(profile)
            
            # Save updated configuration
            self._save_scope_config(ConfigScope.PROJECT)
            
            return True
            
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return False
    
    def reset_configuration(self, scope: ConfigScope = ConfigScope.PROJECT):
        """Reset configuration to defaults"""
        
        # Default configuration
        defaults = {
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
        
        # Reset to defaults
        self.system_config = SystemConfig(**defaults)
        
        # Apply IDE defaults again
        self._apply_ide_defaults()
        
        # Save reset configuration
        self._save_scope_config(scope)
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        return {
            "ide_info": self.ide_detector.to_dict(),
            "system_config": {
                "ide_detection": self.system_config.ide_detection,
                "skill_discovery": self.system_config.skill_discovery,
                "ai_routing": self.system_config.ai_routing,
                "performance": self.system_config.performance,
                "security": self.system_config.security,
                "logging": self.system_config.logging,
                "integration": self.system_config.integration
            },
            "profiles": {
                name: {
                    "scope": profile.scope.value,
                    "active": profile.active,
                    "description": profile.description,
                    "settings_count": len(profile.settings)
                } for name, profile in self.profiles.items()
            },
            "configuration_files": {
                "global": str(self.global_config_path),
                "workspace": str(self.workspace_config_path),
                "project": str(self.project_config_path),
                "user": str(self.user_config_path)
            }
        }

def main():
    """Test the configuration manager"""
    agent_root = Path.cwd() / ".agent"
    config_manager = ConfigManager(agent_root)
    
    print("🔧 Enhanced Configuration System")
    print("=" * 40)
    
    # Show configuration summary
    summary = config_manager.get_configuration_summary()
    print(f"IDE: {summary['ide_info']['ide']['name']}")
    print(f"Platform: {summary['ide_info']['system']['platform']}")
    print(f"Profiles: {len(summary['profiles'])}")
    
    # Validate configuration
    validation = config_manager.validate_configuration()
    print(f"Configuration valid: {validation['valid']}")
    print(f"Health score: {validation['health_score']}")
    
    if validation['issues']:
        print("Issues:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    if validation['warnings']:
        print("Warnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    # Optimize configuration
    optimization = config_manager.optimize_configuration()
    print(f"\nOptimizations applied: {len(optimization['optimizations'])}")
    for opt in optimization['optimizations']:
        print(f"  - {opt}")
    
    # Export configuration
    export_path = agent_root / "config_export.json"
    if config_manager.export_configuration(export_path):
        print(f"\nConfiguration exported to: {export_path}")

if __name__ == "__main__":
    main()
