#!/usr/bin/env python3
"""
Universal IDE Compatibility Layer - Enhanced VS Code Agent System
==================================================================

Detects the current IDE environment and provides compatibility adapters
for VS Code-based IDEs (Windsurf, Cursor, Code, etc.).

Supported IDEs:
- VS Code
- Windsurf
- Cursor
- Continue.dev
- Codeium
- Other VS Code-based editors
"""

import os
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class IDEType(Enum):
    VSCODE = "vscode"
    WINDSURF = "windsurf"
    CURSOR = "cursor"
    CONTINUE = "continue"
    CODEIUM = "codeium"
    UNKNOWN = "unknown"

@dataclass
class IDEInfo:
    name: str
    type: IDEType
    version: Optional[str] = None
    platform: str = ""
    capabilities: List[str] = None
    config_paths: Dict[str, str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.config_paths is None:
            self.config_paths = {}

class IDEDetector:
    """Universal IDE detection and compatibility system"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.ide_info = self._detect_ide()
        
    def _get_system_info(self) -> Dict[str, str]:
        """Get system platform information"""
        return {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "home": str(Path.home())
        }
    
    def _detect_ide(self) -> IDEInfo:
        """Detect the current IDE environment"""
        # Check environment variables
        env_indicators = self._check_environment_indicators()
        
        # Check running processes
        process_indicators = self._check_process_indicators()
        
        # Check configuration files
        config_indicators = self._check_config_indicators()
        
        # Determine IDE type
        ide_type = self._determine_ide_type(env_indicators, process_indicators, config_indicators)
        
        # Get IDE-specific information
        return self._get_ide_info(ide_type)
    
    def _check_environment_indicators(self) -> Dict[str, str]:
        """Check environment variables for IDE indicators"""
        indicators = {}
        
        # Common IDE environment variables
        env_checks = {
            "VSCODE_PID": IDEType.VSCODE,
            "VSCODE_IPC_HOOK": IDEType.VSCODE,
            "WINDSURF_PID": IDEType.WINDSURF,
            "WINDSURF_IPC_HOOK": IDEType.WINDSURF,
            "CURSOR_PID": IDEType.CURSOR,
            "CURSOR_IPC_HOOK": IDEType.CURSOR,
            "CONTINUE_PID": IDEType.CONTINUE,
            "CODEIUM_PID": IDEType.CODEIUM
        }
        
        for env_var, ide_type in env_checks.items():
            if env_var in os.environ:
                indicators[env_var] = os.environ[env_var]
                
        return indicators
    
    def _check_process_indicators(self) -> List[str]:
        """Check running processes for IDE indicators"""
        processes = []
        
        try:
            if self.system_info["platform"] == "Darwin":  # macOS
                result = os.popen("ps aux | grep -E '(vscode|windsurf|cursor|continue|codeium)' | grep -v grep").read()
                processes = [line.strip() for line in result.split('\n') if line.strip()]
            elif self.system_info["platform"] == "Linux":
                result = os.popen("ps aux | grep -E '(vscode|windsurf|cursor|continue|codeium)' | grep -v grep").read()
                processes = [line.strip() for line in result.split('\n') if line.strip()]
            elif self.system_info["platform"] == "Windows":
                result = os.popen('tasklist | findstr /i "code.exe windsurf.exe cursor.exe"').read()
                processes = [line.strip() for line in result.split('\n') if line.strip()]
        except Exception:
            pass
            
        return processes
    
    def _check_config_indicators(self) -> Dict[str, Path]:
        """Check configuration files for IDE indicators"""
        configs = {}
        home = Path.home()
        
        # Common config paths
        config_paths = {
            ".vscode": home / ".vscode",
            ".windsurf": home / ".windsurf", 
            ".cursor": home / ".cursor",
            ".continue": home / ".continue",
            "AppData/Local/Programs": Path.home() / "AppData" / "Local" / "Programs" if self.system_info["platform"] == "Windows" else None,
            "Applications": Path("/Applications") if self.system_info["platform"] == "Darwin" else None,
            "/usr/bin": Path("/usr/bin") if self.system_info["platform"] == "Linux" else None
        }
        
        for name, path in config_paths.items():
            if path and path.exists():
                configs[name] = path
                
        return configs
    
    def _determine_ide_type(self, env_indicators: Dict, process_indicators: List, config_indicators: Dict) -> IDEType:
        """Determine IDE type based on all indicators"""
        
        # Priority 1: Environment variables
        for env_var, value in env_indicators.items():
            if "WINDSURF" in env_var:
                return IDEType.WINDSURF
            elif "CURSOR" in env_var:
                return IDEType.CURSOR
            elif "CONTINUE" in env_var:
                return IDEType.CONTINUE
            elif "CODEIUM" in env_var:
                return IDEType.CODEIUM
            elif "VSCODE" in env_var:
                return IDEType.VSCODE
        
        # Priority 2: Process names
        process_text = " ".join(process_indicators).lower()
        if "windsurf" in process_text:
            return IDEType.WINDSURF
        elif "cursor" in process_text:
            return IDEType.CURSOR
        elif "continue" in process_text:
            return IDEType.CONTINUE
        elif "codeium" in process_text:
            return IDEType.CODEIUM
        elif "vscode" in process_text or "visual studio code" in process_text:
            return IDEType.VSCODE
        
        # Priority 3: Configuration files
        if ".windsurf" in config_indicators:
            return IDEType.WINDSURF
        elif ".cursor" in config_indicators:
            return IDEType.CURSOR
        elif ".continue" in config_indicators:
            return IDEType.CONTINUE
        elif ".vscode" in config_indicators:
            return IDEType.VSCODE
        
        return IDEType.UNKNOWN
    
    def _get_ide_info(self, ide_type: IDEType) -> IDEInfo:
        """Get detailed IDE information"""
        
        ide_configs = {
            IDEType.VSCODE: {
                "name": "Visual Studio Code",
                "capabilities": ["extensions", "tasks", "debug", "terminal", "settings"],
                "config_paths": {
                    "settings": str(Path.home() / ".vscode" / "settings.json"),
                    "extensions": str(Path.home() / ".vscode" / "extensions"),
                    "tasks": str(Path.home() / ".vscode" / "tasks.json")
                }
            },
            IDEType.WINDSURF: {
                "name": "Windsurf",
                "capabilities": ["ai-assistant", "cascading", "extensions", "tasks", "debug", "terminal"],
                "config_paths": {
                    "settings": str(Path.home() / ".windsurf" / "settings.json"),
                    "extensions": str(Path.home() / ".windsurf" / "extensions"),
                    "agent": str(Path.home() / ".windsurf" / "agent")
                }
            },
            IDEType.CURSOR: {
                "name": "Cursor",
                "capabilities": ["ai-coding", "extensions", "tasks", "debug", "terminal"],
                "config_paths": {
                    "settings": str(Path.home() / ".cursor" / "settings.json"),
                    "extensions": str(Path.home() / ".cursor" / "extensions")
                }
            },
            IDEType.CONTINUE: {
                "name": "Continue.dev",
                "capabilities": ["ai-assistant", "extensions", "custom-models"],
                "config_paths": {
                    "config": str(Path.home() / ".continue" / "config.json")
                }
            },
            IDEType.CODEIUM: {
                "name": "Codeium",
                "capabilities": ["ai-autocomplete", "extensions", "chat"],
                "config_paths": {
                    "settings": str(Path.home() / ".codeium" / "settings.json")
                }
            },
            IDEType.UNKNOWN: {
                "name": "Unknown IDE",
                "capabilities": ["basic"],
                "config_paths": {}
            }
        }
        
        config = ide_configs.get(ide_type, ide_configs[IDEType.UNKNOWN])
        
        return IDEInfo(
            name=config["name"],
            type=ide_type,
            platform=self.system_info["platform"],
            capabilities=config["capabilities"],
            config_paths=config["config_paths"]
        )
    
    def get_compatibility_adapter(self) -> Dict[str, Any]:
        """Get compatibility adapter for the detected IDE"""
        
        adapters = {
            IDEType.VSCODE: {
                "file_operations": "standard",
                "command_palette": "vscode",
                "extension_api": "vscode",
                "workspace_folders": "vscode",
                "terminal_integration": "integrated"
            },
            IDEType.WINDSURF: {
                "file_operations": "enhanced",
                "command_palette": "windsurf",
                "extension_api": "vscode-compatible",
                "workspace_folders": "windsurf",
                "terminal_integration": "cascading",
                "ai_features": "native"
            },
            IDEType.CURSOR: {
                "file_operations": "ai-enhanced",
                "command_palette": "cursor",
                "extension_api": "vscode-compatible",
                "workspace_folders": "cursor",
                "terminal_integration": "ai-integrated"
            },
            IDEType.CONTINUE: {
                "file_operations": "standard",
                "command_palette": "continue",
                "extension_api": "custom",
                "workspace_folders": "standard",
                "terminal_integration": "standard"
            },
            IDEType.CODEIUM: {
                "file_operations": "standard",
                "command_palette": "codeium",
                "extension_api": "vscode-compatible",
                "workspace_folders": "standard",
                "terminal_integration": "standard"
            },
            IDEType.UNKNOWN: {
                "file_operations": "basic",
                "command_palette": "generic",
                "extension_api": "none",
                "workspace_folders": "basic",
                "terminal_integration": "external"
            }
        }
        
        return adapters.get(self.ide_info.type, adapters[IDEType.UNKNOWN])
    
    def get_agent_config_path(self) -> Path:
        """Get the appropriate agent configuration path for the current IDE"""
        
        base_configs = {
            IDEType.WINDSURF: Path.home() / ".windsurf" / "agent",
            IDEType.CURSOR: Path.home() / ".cursor" / "agent",
            IDEType.VSCODE: Path.cwd() / ".agent",
            IDEType.CONTINUE: Path.cwd() / ".agent",
            IDEType.CODEIUM: Path.cwd() / ".agent"
        }
        
        return base_configs.get(self.ide_info.type, Path.cwd() / ".agent")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert IDE info to dictionary"""
        return {
            "ide": {
                "name": self.ide_info.name,
                "type": self.ide_info.type.value,
                "platform": self.ide_info.platform,
                "capabilities": self.ide_info.capabilities,
                "config_paths": self.ide_info.config_paths
            },
            "system": self.system_info,
            "compatibility": self.get_compatibility_adapter(),
            "agent_config_path": str(self.get_agent_config_path())
        }

def main():
    """Main function for testing"""
    detector = IDEDetector()
    print(json.dumps(detector.to_dict(), indent=2))

if __name__ == "__main__":
    main()
