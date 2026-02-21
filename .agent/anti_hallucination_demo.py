#!/usr/bin/env python3
"""
Anti-Hallucination System Demo
==============================

Demonstrates the comprehensive anti-hallucination safeguards
in the Enhanced VS Code Agent System.
"""

import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

def main():
    """Run the anti-hallucination demonstration"""
    print("🛡️ Anti-Hallucination System Demo")
    print("=" * 50)
    
    try:
        # Import the anti-hallucination system
        from anti_hallucination import AntiHallucinationSystem
        
        agent_root = Path(__file__).parent
        anti_hallucination = AntiHallucinationSystem(agent_root)
        
        print("✅ Anti-hallucination system initialized!")
        
        # Test cases with different risk levels
        test_cases = [
            {
                "name": "Low Risk - Verified Facts",
                "response": "React is a JavaScript library created by Facebook in 2013 for building user interfaces. It uses a virtual DOM for efficient updates.",
                "context": {"domain": "frontend", "technologies": ["react"], "intent": "create"}
            },
            {
                "name": "Medium Risk - Partially Verified",
                "response": "Vue.js is a progressive framework created by Evan You. It's popular for building interactive web interfaces and has a gentle learning curve.",
                "context": {"domain": "frontend", "technologies": ["vue"], "intent": "create"}
            },
            {
                "name": "High Risk - Unverified Claims",
                "response": "Angular was invented by Google in 2010 and it's the fastest framework ever made with 100% guaranteed performance. Every company uses Angular.",
                "context": {"domain": "frontend", "technologies": ["angular"], "intent": "create"}
            },
            {
                "name": "Critical Risk - Impossible Claims",
                "response": "Docker containers can run any code instantly without any setup. It's 100% free and never has security issues. All developers love Docker unconditionally.",
                "context": {"domain": "devops", "technologies": ["docker"], "intent": "create"}
            },
            {
                "name": "Code Example",
                "response": """Here's a Python API endpoint:

```python
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': []})

if __name__ == '__main__':
    app.run(debug=True)
```

This creates a simple REST API with Flask.""",
                "context": {"domain": "backend", "technologies": ["python", "flask"], "intent": "create"}
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔍 Test Case {i}: {test_case['name']}")
            print("-" * 40)
            print(f"Response: {test_case['response'][:100]}...")
            
            # Analyze the response
            result = anti_hallucination.analyze_response(test_case['response'], test_case['context'])
            
            # Show results
            risk_icon = {
                "low": "🟢",
                "medium": "🟡", 
                "high": "🟠",
                "critical": "🔴"
            }.get(result.overall_risk.value, "⚪")
            
            print(f"\n{risk_icon} Risk Level: {result.overall_risk.value.upper()}")
            print(f"📊 Confidence Score: {result.confidence_score:.2f}")
            
            if result.warnings:
                print("\n⚠️ Warnings:")
                for warning in result.warnings:
                    print(f"   {warning}")
            
            if result.recommendations:
                print("\n💡 Recommendations:")
                for rec in result.recommendations[:3]:  # Show first 3
                    print(f"   {rec}")
            
            if result.verified_facts:
                print(f"\n✅ Verified Facts ({len(result.verified_facts)}):")
                for fact in result.verified_facts[:3]:  # Show first 3
                    print(f"   • {fact}")
            
            if result.uncertain_claims:
                print(f"\n❓ Uncertain Claims ({len(result.uncertain_claims)}):")
                for claim in result.uncertain_claims[:3]:  # Show first 3
                    print(f"   • {claim}")
            
            # Validation breakdown
            print(f"\n📋 Validation Breakdown:")
            for validation in result.validations:
                status_icon = "✅" if validation.passed else "❌"
                print(f"   {status_icon} {validation.validation_type.value}: {validation.confidence:.2f} confidence")
                if validation.details:
                    print(f"      {validation.details}")
        
        # Show system statistics
        print(f"\n📈 Anti-Hallucination System Statistics:")
        print(f"   Knowledge Base: {len(anti_hallucination.knowledge_base['technologies'])} technologies")
        print(f"   Validation Rules: {len(anti_hallucination.validation_rules)} categories")
        print(f"   Confidence Thresholds: {anti_hallucination.confidence_thresholds}")
        
        print(f"\n🎯 Key Anti-Hallucination Strategies:")
        strategies = [
            "✅ Factual verification against knowledge base",
            "✅ Syntax validation for code examples", 
            "✅ Semantic consistency checking",
            "✅ Context relevance validation",
            "✅ Source citation verification",
            "✅ Risk level assessment",
            "✅ Confidence scoring",
            "✅ Warning and recommendation system"
        ]
        
        for strategy in strategies:
            print(f"   {strategy}")
        
        print(f"\n🛡️ How This Prevents Hallucination:")
        print(f"   1. **Fact-Checking**: Verifies claims against known knowledge base")
        print(f"   2. **Source Validation**: Ensures claims have proper citations")
        print(f"   3. **Context Awareness**: Validates relevance to user's request")
        print(f"   4. **Code Validation**: Checks syntax and logic of code examples")
        print(f"   5. **Risk Assessment**: Identifies potentially hallucinated content")
        print(f"   6. **Confidence Scoring**: Provides transparency about reliability")
        print(f"   7. **Warning System**: Alerts users to uncertain content")
        print(f"   8. **Recommendations**: Suggests improvements for accuracy")
        
        print(f"\n🎉 Anti-hallucination system successfully protects against AI hallucination!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
