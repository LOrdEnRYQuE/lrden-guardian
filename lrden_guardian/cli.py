#!/usr/bin/env python3
"""
LRDEnE Guardian - Command Line Interface
=======================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Command line interface for LRDEnE Guardian AI safety system.
"""

import argparse
import sys
import json
from typing import Dict, Any, Optional
from pathlib import Path

from .guardian import create_lrden_guardian, LRDEnEGuardian
from . import __version__, get_package_info

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    
    parser = argparse.ArgumentParser(
        prog="lrden-guardian",
        description="LRDEnE Guardian - Advanced AI Safety & Hallucination Detection System",
        epilog="Copyright (c) 2026 LRDEnE. All rights reserved.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"LRDEnE Guardian v{__version__}"
    )
    
    parser.add_argument(
        "--license-key",
        type=str,
        help="LRDEnE Guardian license key for premium features"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze content for safety and hallucinations"
    )
    analyze_parser.add_argument(
        "content",
        help="Content to analyze (file path or text)"
    )
    analyze_parser.add_argument(
        "--context",
        type=str,
        help="Context for analysis (JSON format)"
    )
    analyze_parser.add_argument(
        "--output",
        choices=["json", "text", "summary"],
        default="summary",
        help="Output format"
    )
    analyze_parser.add_argument(
        "--file",
        action="store_true",
        help="Treat content as file path"
    )
    
    # Check command
    check_parser = subparsers.add_parser(
        "check",
        help="Quick safety check of content"
    )
    check_parser.add_argument(
        "content",
        help="Content to check (file path or text)"
    )
    check_parser.add_argument(
        "--file",
        action="store_true",
        help="Treat content as file path"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Display LRDEnE Guardian system information"
    )
    
    # Demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run LRDEnE Guardian demonstration"
    )
    demo_parser.add_argument(
        "--scenario",
        choices=["enterprise", "security", "education", "marketing", "ai"],
        help="Specific demo scenario to run"
    )
    
    return parser

def load_content(content: str, is_file: bool = False) -> str:
    """Load content from file or direct input"""
    
    if is_file:
        try:
            with open(content, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ Error: File '{content}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    else:
        return content

def parse_context(context_str: Optional[str]) -> Dict[str, Any]:
    """Parse context from JSON string"""
    
    if not context_str:
        return {}
    
    try:
        return json.loads(context_str)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing context JSON: {e}")
        sys.exit(1)

def format_output(result, output_format: str = "summary") -> str:
    """Format analysis result for output"""
    
    if output_format == "json":
        return json.dumps({
            "is_safe": result.is_safe,
            "risk_level": result.risk_level.value,
            "confidence_score": result.confidence_score,
            "guardian_score": result.guardian_score,
            "analysis_summary": result.analysis_summary,
            "recommendations": result.recommendations,
            "detected_issues": result.detected_issues,
            "uncertainty_areas": result.uncertainty_areas,
            "metadata": result.metadata
        }, indent=2)
    
    elif output_format == "text":
        output = []
        output.append("🛡️ LRDEnE Guardian Analysis Results")
        output.append("=" * 40)
        output.append(f"✅ Content Safe: {'YES' if result.is_safe else 'NO'}")
        output.append(f"📊 Risk Level: {result.risk_level.value.upper()}")
        output.append(f"🔍 Confidence: {result.confidence_score:.2f}")
        output.append(f"⭐ Guardian Score: {result.guardian_score:.3f}")
        output.append(f"📝 Summary: {result.analysis_summary}")
        
        if result.recommendations:
            output.append("\n💡 LRDEnE Recommendations:")
            for rec in result.recommendations:
                output.append(f"   • {rec}")
        
        if result.detected_issues:
            output.append("\n🚨 Detected Issues:")
            for issue in result.detected_issues[:5]:
                output.append(f"   • {issue}")
        
        return "\n".join(output)
    
    else:  # summary
        status = "✅ SAFE" if result.is_safe else "🚨 REQUIRES REVIEW"
        return f"{status} | Risk: {result.risk_level.value.upper()} | Confidence: {result.confidence_score:.2f} | Guardian Score: {result.guardian_score:.3f}"

def cmd_analyze(args) -> None:
    """Handle analyze command"""
    
    # Load content
    content = load_content(args.content, args.file)
    
    # Parse context
    context = parse_context(args.context)
    
    # Initialize Guardian
    guardian = create_lrden_guardian(license_key=args.license_key)
    
    # Analyze content
    print("🛡️ Analyzing content with LRDEnE Guardian...")
    result = guardian.analyze_content(content, context)
    
    # Output results
    output = format_output(result, args.output)
    print(output)

def cmd_check(args) -> None:
    """Handle check command"""
    
    # Load content
    content = load_content(args.content, args.file)
    
    # Initialize Guardian
    guardian = create_lrden_guardian(license_key=args.license_key)
    
    # Quick check
    result = guardian.analyze_content(content)
    
    # Simple output
    status = "✅ SAFE" if result.is_safe else "🚨 RISK DETECTED"
    print(f"{status} | Guardian Score: {result.guardian_score:.3f}")
    
    if not result.is_safe:
        print(f"🔍 Risk Level: {result.risk_level.value.upper()}")
        print(f"💡 Top Issues: {', '.join(result.detected_issues[:3])}")

def cmd_info(args) -> None:
    """Handle info command"""
    
    print("🛡️ LRDEnE Guardian System Information")
    print("=" * 40)
    
    # Package info
    info = get_package_info()
    for key, value in info.items():
        if key != "documentation":
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Guardian info
    guardian = create_lrden_guardian()
    guardian_info = guardian.get_guardian_info()
    
    print(f"\n🔧 Guardian Capabilities:")
    for capability in guardian_info["capabilities"]:
        print(f"   • {capability}")

def cmd_demo(args) -> None:
    """Handle demo command"""
    
    from .demo import LRDEnEGuardianDemo
    
    print("🛡️ LRDEnE Guardian Demonstration")
    print("=" * 40)
    
    demo = LRDEnEGuardianDemo()
    
    if args.scenario:
        # Run specific scenario
        scenario_methods = {
            "enterprise": demo.test_enterprise_content,
            "security": demo.test_security_compliance,
            "education": demo.test_educational_content,
            "marketing": demo.test_marketing_claims,
            "ai": demo.test_ai_safety
        }
        
        if args.scenario in scenario_methods:
            result = scenario_methods[args.scenario]()
            print(f"✅ Demo completed for {args.scenario} scenario")
        else:
            print(f"❌ Unknown scenario: {args.scenario}")
    else:
        # Run full demo
        demo.run_brand_showcase()

def main() -> None:
    """Main CLI entry point"""
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "analyze":
            cmd_analyze(args)
        elif args.command == "check":
            cmd_check(args)
        elif args.command == "info":
            cmd_info(args)
        elif args.command == "demo":
            cmd_demo(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🛡️ LRDEnE Guardian analysis interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
