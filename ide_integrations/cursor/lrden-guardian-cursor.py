#!/usr/bin/env python3
"""
LRDEnE Guardian - Cursor IDE Integration
========================================

Copyright (c) 2026 LRDEnE. All rights reserved.

AI safety and hallucination detection for Cursor IDE.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    exit(1)

@dataclass
class CursorIntegration:
    """Cursor IDE integration configuration"""
    api_endpoint: str = "http://localhost:5001"
    auto_analyze: bool = True
    analysis_delay: float = 1.0
    supported_languages: List[str] = None
    risk_threshold: str = "medium"
    show_notifications: bool = True
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust", "php", "ruby", "markdown"]

class LRDEnEGuardianCursor:
    """LRDEnE Guardian integration for Cursor IDE"""
    
    def __init__(self, config: Optional[CursorIntegration] = None):
        self.config = config or CursorIntegration()
        self.cache = {}
        self.config_file = Path.home() / ".cursor" / "lrden-guardian.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
        self.setup_cursor_integration()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    # Update config with loaded data
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
        except Exception as e:
            print(f"Error loading Cursor config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_data = {
                "api_endpoint": self.config.api_endpoint,
                "auto_analyze": self.config.auto_analyze,
                "analysis_delay": self.config.analysis_delay,
                "supported_languages": self.config.supported_languages,
                "risk_threshold": self.config.risk_threshold,
                "show_notifications": self.config.show_notifications
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving Cursor config: {e}")
    
    def setup_cursor_integration(self):
        """Setup Cursor IDE integration"""
        # Create Cursor-specific configuration
        cursor_config_dir = Path.home() / ".cursor"
        cursor_config_dir.mkdir(exist_ok=True)
        
        # Create .cursorrules file for auto-analysis
        cursor_rules_file = cursor_config_dir / ".cursorrules"
        if not cursor_rules_file.exists():
            self.create_cursor_rules(cursor_rules_file)
        
        # Create integration script
        integration_script = cursor_config_dir / "lrden-guardian-integration.py"
        self.create_integration_script(integration_script)
        
        print("✅ LRDEnE Guardian Cursor integration setup complete!")
        print(f"📁 Config file: {self.config_file}")
        print(f"📁 Cursor rules: {cursor_rules_file}")
        print(f"📁 Integration script: {integration_script}")
    
    def create_cursor_rules(self, rules_file: Path):
        """Create Cursor rules for auto-analysis"""
        rules = {
            "description": "LRDEnE Guardian AI Safety Rules",
            "version": "1.0.0",
            "rules": [
                {
                    "name": "Analyze AI-generated code",
                    "description": "Automatically analyze code that appears to be AI-generated",
                    "pattern": ".*",
                    "action": "analyze_with_guardian",
                    "conditions": [
                        "contains_ai_indicators",
                        "file_size_gt_100",
                        "supported_language"
                    ]
                },
                {
                    "name": "Check for hallucinations",
                    "description": "Flag potential AI hallucinations in code",
                    "pattern": ".*",
                    "action": "check_hallucinations",
                    "conditions": [
                        "contains_hallucination_patterns",
                        "has_uncertain_statements"
                    ]
                }
            ],
            "ai_indicators": [
                "As an AI language model",
                "I cannot provide",
                "I don't have access",
                "As an AI assistant",
                "I'm an AI",
                "I am an AI"
            ],
            "hallucination_patterns": [
                "definitely",
                "absolutely certain",
                "without any doubt",
                "guaranteed to work",
                "always succeeds",
                "never fails",
                "perfectly accurate"
            ],
            "supported_languages": self.config.supported_languages
        }
        
        with open(rules_file, 'w') as f:
            json.dump(rules, f, indent=2)
    
    def create_integration_script(self, script_file: Path):
        """Create integration script for Cursor"""
        script_content = f'''#!/usr/bin/env python3
"""
LRDEnE Guardian Cursor Integration Script
======================================

This script integrates LRDEnE Guardian with Cursor IDE
for real-time AI safety analysis.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Add the universal integration to path
sys.path.insert(0, "{Path(__file__).parent.parent.parent / 'general'}")

try:
    from lrden_guardian_universal import LRDEnEGuardianUniversal
except ImportError:
    print("Error: LRDEnE Guardian universal integration not found")
    sys.exit(1)

class CursorIntegrationManager:
    def __init__(self):
        self.guardian = LRDEnEGuardianUniversal("{self.config.api_endpoint}")
        self.cursor_dir = Path.home() / ".cursor"
        self.rules_file = self.cursor_dir / ".cursorrules"
        self.load_rules()
    
    def load_rules(self):
        """Load analysis rules"""
        try:
            with open(self.rules_file, 'r') as f:
                self.rules = json.load(f)
        except Exception as e:
            print(f"Error loading rules: {{e}}")
            self.rules = {{}}
    
    def should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed"""
        file_ext = Path(file_path).suffix.lower()
        
        # Check if file extension is supported
        if file_ext not in self.rules.get("supported_languages", []):
            return False
        
        # Check file size
        try:
            file_size = os.path.getsize(file_path)
            if file_size < 100:  # bytes
                return False
        except:
            return False
        
        return True
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file and return results"""
        if not self.should_analyze_file(file_path):
            return {{"skipped": True, "reason": "File not supported for analysis"}}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for AI indicators
            ai_indicators = self.rules.get("ai_indicators", [])
            has_ai_indicators = any(indicator.lower() in content.lower() for indicator in ai_indicators)
            
            # Check for hallucination patterns
            hallucination_patterns = self.rules.get("hallucination_patterns", [])
            has_hallucination = any(pattern.lower() in content.lower() for pattern in hallucination_patterns)
            
            # Call Guardian API
            result = self.guardian.analyze_file(file_path)
            
            # Add additional analysis
            if "error" not in result:
                result["ai_indicators_detected"] = has_ai_indicators
                result["hallucination_patterns_detected"] = has_hallucination
                result["requires_review"] = not result.get("is_safe", True) or has_ai_indicators or has_hallucination
            
            return result
            
        except Exception as e:
            return {{"error": f"Analysis failed: {{str(e)}}"}
    
    def monitor_cursor_workspace(self):
        """Monitor Cursor workspace for changes"""
        print("🛡️ LRDEnE Guardian - Monitoring Cursor workspace...")
        print("Press Ctrl+C to stop monitoring")
        
        # Get Cursor workspace directory
        workspace_dir = self.get_cursor_workspace()
        if not workspace_dir:
            print("❌ Could not determine Cursor workspace directory")
            return
        
        print(f"📁 Monitoring: {{workspace_dir}}")
        
        # Monitor for file changes
        try:
            import watchdog.observers
            from watchdog.events import FileSystemEventHandler
            
            class GuardianFileHandler(FileSystemEventHandler):
                def __init__(self, manager):
                    self.manager = manager
                
                def on_modified(self, event):
                    if not event.is_directory:
                        self.handle_file_change(event.src_path)
                
                def handle_file_change(self, file_path):
                    if self.manager.should_analyze_file(file_path):
                        print(f"🔍 Analyzing: {{file_path}}")
                        result = self.manager.analyze_file(file_path)
                        self.display_result(result, file_path)
                
                def display_result(self, result, file_path):
                    if "error" in result:
                        print(f"❌ {{result['error']}}")
                    elif result.get("requires_review", False):
                        print(f"⚠️ {{file_path}} - REQUIRES REVIEW")
                        print(f"   Risk: {{result.get('risk_level', 'unknown')}}")
                        print(f"   Score: {{result.get('guardian_score', 0):.3f}}")
                        if result.get("detected_issues"):
                            for issue in result.get("detected_issues", [])[:3]:
                                print(f"   • {{issue}}")
                    else:
                        print(f"✅ {{file_path}} - SAFE")
            
            observer = watchdog.observers.Observer()
            event_handler = GuardianFileHandler(self)
            observer.schedule(event_handler, workspace_dir, recursive=True)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\\n🛡️ Monitoring stopped")
                
        except ImportError:
            print("❌ Watchdog library not found. Install with: pip install watchdog")
            print("Falling back to manual analysis mode")
    
    def get_cursor_workspace(self) -> Optional[str]:
        """Get Cursor workspace directory"""
        # Try environment variables first
        workspace_dir = os.environ.get('CURSOR_FOLDER')
        if workspace_dir and os.path.exists(workspace_dir):
            return workspace_dir
        
        # Try common locations
        home_dir = Path.home()
        possible_dirs = [
            home_dir / "Cursor",
            home_dir / "cursor",
            home_dir / ".cursor",
            Path("/opt/cursor"),
            Path("/usr/local/cursor")
        ]
        
        for dir_path in possible_dirs:
            if dir_path.exists():
                return str(dir_path)
        
        return None

if __name__ == "__main__":
    manager = CursorIntegrationManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        manager.monitor_cursor_workspace()
    else:
        print("🛡️ LRDEnE Guardian - Cursor Integration")
        print("Usage:")
        print("  python lrden-guardian-integration.py monitor  # Monitor workspace")
        print("  python lrden-guardian-integration.py analyze <file>  # Analyze specific file")
        
        if len(sys.argv) > 2 and sys.argv[1] == "analyze":
            file_path = sys.argv[2]
            if os.path.exists(file_path):
                result = manager.analyze_file(file_path)
                print(f"📊 Analysis Results for {{file_path}}:")
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ File not found: {{file_path}}")
'''
        
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_file, 0o755)
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file"""
        return self.guardian.analyze_file(file_path)
    
    def check_connection(self) -> bool:
        """Check if Guardian API is accessible"""
        return self.guardian.check_connection()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LRDEnE Guardian - Cursor IDE Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        choices=["setup", "analyze", "monitor", "check"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="File to analyze"
    )
    
    parser.add_argument(
        "--endpoint", "-e",
        default="http://localhost:5001",
        help="LRDEnE Guardian API endpoint"
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == "setup":
            integration = LRDEnEGuardianCursor()
            integration.setup_cursor_integration()
        
        elif args.command == "analyze":
            if not args.file:
                print("❌ Please provide a file to analyze")
                return
            
            integration = LRDEnEGuardianCursor()
            if os.path.exists(args.file):
                result = integration.analyze_file(args.file)
                print("🛡️ LRDEnE Guardian Analysis Results")
                print("=" * 40)
                print(f"File: {args.file}")
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ File not found: {args.file}")
        
        elif args.command == "monitor":
            integration = LRDEnEGuardianCursor()
            integration.monitor_cursor_workspace()
        
        elif args.command == "check":
            integration = LRDEnEGuardianCursor()
            if integration.check_connection():
                print("✅ LRDEnE Guardian API is accessible")
            else:
                print("❌ LRDEnE Guardian API is not accessible")
                print(f"   Endpoint: {args.endpoint}")
    
    except KeyboardInterrupt:
        print("\\nOperation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
'''
