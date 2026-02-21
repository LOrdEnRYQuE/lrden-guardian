#!/usr/bin/env python3
"""
LRDEnE Guardian - Universal IDE Integration
==========================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Universal integration for IDEs that support external tools or scripts.
Works with Cursor, Windsurf, Antigravity, Bolt, Lovable, and more.
"""

import os
import sys
import json
import argparse
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

class LRDEnEGuardianUniversal:
    """Universal IDE integration for LRDEnE Guardian"""
    
    def __init__(self, api_endpoint: str = "http://localhost:5001"):
        self.api_endpoint = api_endpoint
        self.cache = {}
        self.config_file = Path.home() / ".lrden-guardian" / "config.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "api_endpoint": self.api_endpoint,
                    "auto_analyze": True,
                    "supported_extensions": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".php", ".rb", ".md"],
                    "risk_threshold": "medium",
                    "show_notifications": True
                }
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file"""
        try:
            # Check cache first
            cache_key = f"{file_path}:{os.path.getmtime(file_path)}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip very short files
            if len(content.strip()) < 10:
                return {"error": "File too short for analysis"}
            
            # Call Guardian API
            response = requests.post(
                f"{self.api_endpoint}/analyze",
                json={
                    "content": content,
                    "context": {
                        "source": "universal_ide_integration",
                        "file_path": file_path,
                        "file_extension": Path(file_path).suffix,
                        "ide": os.environ.get('IDE_NAME', 'unknown'),
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                analysis = response.json
                
                # Cache result
                self.cache[cache_key] = analysis
                
                # Limit cache size
                if len(self.cache) > 1000:
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
                
                return analysis
            else:
                return {"error": f"API request failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def analyze_text(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze text content"""
        try:
            if len(text.strip()) < 10:
                return {"error": "Text too short for analysis"}
            
            response = requests.post(
                f"{self.api_endpoint}/analyze",
                json={
                    "content": text,
                    "context": {
                        **(context or {}),
                        "source": "universal_ide_integration",
                        "ide": os.environ.get('IDE_NAME', 'unknown'),
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API request failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def check_connection(self) -> bool:
        """Check if Guardian API is accessible"""
        try:
            response = requests.get(f"{self.api_endpoint}/api-info", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "api_endpoint": self.config.get("api_endpoint", self.api_endpoint),
            "connected": self.check_connection(),
            "cache_size": len(self.cache),
            "config_file": str(self.config_file),
            "supported_extensions": self.config.get("supported_extensions", []),
            "ide": os.environ.get('IDE_NAME', 'unknown')
        }

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="LRDEnE Guardian - Universal IDE Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        choices=["analyze", "check", "status", "config"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="File to analyze"
    )
    
    parser.add_argument(
        "--text", "-t",
        help="Text to analyze"
    )
    
    parser.add_argument(
        "--endpoint", "-e",
        default="http://localhost:5001",
        help="LRDEnE Guardian API endpoint"
    )
    
    parser.add_argument(
        "--output", "-o",
        choices=["json", "text", "summary"],
        default="summary",
        help="Output format"
    )
    
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Show cache information"
    )
    
    args = parser.parse_args()
    
    # Set IDE name from environment
    if not os.environ.get('IDE_NAME'):
        os.environ['IDE_NAME'] = detect_ide()
    
    guardian = LRDEnEGuardianUniversal(args.endpoint)
    
    try:
        if args.command == "analyze":
            if args.file:
                result = guardian.analyze_file(args.file)
            elif args.text:
                result = guardian.analyze_text(args.text)
            else:
                # Read from stdin
                text = sys.stdin.read()
                result = guardian.analyze_text(text)
            
            output_result(result, args.output)
            
        elif args.command == "check":
            if guardian.check_connection():
                print("✅ LRDEnE Guardian API is accessible")
            else:
                print("❌ LRDEnE Guardian API is not accessible")
                print(f"   Endpoint: {args.endpoint}")
                sys.exit(1)
        
        elif args.command == "status":
            status = guardian.get_status()
            print("🛡️ LRDEnE Guardian Status")
            print("=" * 30)
            print(f"API Endpoint: {status['api_endpoint']}")
            print(f"Connected: {'✅' if status['connected'] else '❌'}")
            print(f"Cache Size: {status['cache_size']} items")
            print(f"IDE: {status['ide']}")
            print(f"Config File: {status['config_file']}")
            print(f"Supported Extensions: {', '.join(status['supported_extensions'])}")
        
        elif args.command == "config":
            print("🛡️ LRDEnE Guardian Configuration")
            print("=" * 35)
            print(f"API Endpoint: {guardian.config.get('api_endpoint')}")
            print(f"Auto Analyze: {guardian.config.get('auto_analyze')}")
            print(f"Risk Threshold: {guardian.config.get('risk_threshold')}")
            print(f"Show Notifications: {guardian.config.get('show_notifications')}")
            print(f"Supported Extensions: {', '.join(guardian.config.get('supported_extensions', []))}")
            print(f"Config File: {guardian.config_file}")
            
            if args.cache:
                print(f"\nCache Information:")
                print(f"Size: {len(guardian.cache)} items")
                if guardian.cache:
                    print("Recent Analyses:")
                    for i, (key, analysis) in enumerate(list(guardian.cache.items())[-5:], 1):
                        print(f"  {i}. {key[:50]}... - {analysis.get('risk_level', 'unknown')}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def output_result(result: Dict[str, Any], format_type: str):
    """Format and output analysis result"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    
    if format_type == "json":
        print(json.dumps(result, indent=2))
    elif format_type == "text":
        print("🛡️ LRDEnE Guardian Analysis Results")
        print("=" * 40)
        print(f"Safe: {'✅ YES' if result.get('is_safe') else '❌ NO'}")
        print(f"Risk Level: {result.get('risk_level', 'unknown').upper()}")
        print(f"Guardian Score: {result.get('guardian_score', 0):.3f}")
        print(f"Confidence: {result.get('confidence_score', 0):.1%}")
        print(f"Summary: {result.get('analysis_summary', 'No summary available')}")
        
        if result.get('detected_issues'):
            print("\n🚨 Detected Issues:")
            for issue in result.get('detected_issues', []):
                print(f"  • {issue}")
        
        if result.get('recommendations'):
            print("\n💡 Recommendations:")
            for rec in result.get('recommendations', []):
                print(f"  • {rec}")
    
    else:  # summary
        status = "✅ SAFE" if result.get('is_safe') else "⚠️ RISK"
        risk = result.get('risk_level', 'unknown').upper()
        score = result.get('guardian_score', 0)
        confidence = result.get('confidence_score', 0)
        
        print(f"{status} | Risk: {risk} | Score: {score:.3f} | Confidence: {confidence:.1%}")

def detect_ide() -> str:
    """Detect the current IDE"""
    # Check environment variables
    if os.environ.get('VSCODE_PID'):
        return "VSCode"
    elif os.environ.get('CURSOR_FOLDER'):
        return "Cursor"
    elif os.environ.get('WINDSURF_FOLDER'):
        return "Windsurf"
    elif os.environ.get('ANTIGRAVITY_FOLDER'):
        return "Antigravity"
    elif os.environ.get('BOLT_FOLDER'):
        return "Bolt"
    elif os.environ.get('LOVABLE_FOLDER'):
        return "Lovable"
    
    # Check running processes
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = result.stdout.lower()
        
        if 'cursor' in processes:
            return "Cursor"
        elif 'windsurf' in processes:
            return "Windsurf"
        elif 'antigravity' in processes:
            return "Antigravity"
        elif 'bolt' in processes:
            return "Bolt"
        elif 'lovable' in processes:
            return "Lovable"
        elif 'code' in processes and 'visual studio' not in processes:
            return "VSCode"
    
    except:
        pass
    
    return "Unknown"

if __name__ == "__main__":
    main()
