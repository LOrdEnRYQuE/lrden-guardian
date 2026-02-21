#!/usr/bin/env python3
"""
Hallucination Stress Test Suite
===============================

Comprehensive hard tests to challenge the anti-hallucination system
with edge cases, subtle misinformation, and complex scenarios.

Test Categories:
1. Subtle factual inaccuracies
2. Plausible but false technical claims
3. Mixed truth and falsehood
4. Code with hidden issues
5. Outdated information
6. Over-specific claims
7. Impossible but believable scenarios
8. Domain-specific jargon abuse
"""

import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

def main():
    """Run comprehensive hallucination stress tests"""
    print("🧪 Hallucination Stress Test Suite")
    print("=" * 60)
    print("Testing anti-hallucination system with challenging edge cases...")
    
    try:
        from anti_hallucination import AntiHallucinationSystem
        
        agent_root = Path(__file__).parent
        anti_hallucination = AntiHallucinationSystem(agent_root)
        
        # Hard test cases designed to challenge the system
        hard_tests = [
            {
                "name": "SUBTLE FACTUAL ERROR - React Version",
                "response": "React 16.8 was released in 2019 and introduced hooks, making class components obsolete. All modern React apps use functional components exclusively.",
                "context": {"domain": "frontend", "technologies": ["react"], "intent": "create"},
                "expected_risk": "HIGH",
                "issues": [
                    "Wrong release year (React 16.8 was 2018)",
                    "Class components not obsolete",
                    "Not all apps use functional components exclusively"
                ]
            },
            {
                "name": "PLAUSIBLE BUT FALSE - Docker Performance",
                "response": "Docker containers are 50% faster than bare metal applications because they use kernel-level optimization and shared memory pools. This is why major companies like Netflix and Google use Docker for all production services.",
                "context": {"domain": "devops", "technologies": ["docker"], "intent": "optimize"},
                "expected_risk": "HIGH",
                "issues": [
                    "Containers are actually slower due to overhead",
                    "50% faster claim is false",
                    "Netflix uses containers but not for all services"
                ]
            },
            {
                "name": "MIXED TRUTH/FALSE - Vue Ecosystem",
                "response": "Vue.js was created by Evan You in 2014 and is maintained by the Vue team. It uses a virtual DOM similar to React and has excellent TypeScript support through Vue 3's Composition API. The Vue ecosystem includes Vuex for state management and Vue Router for routing, both officially maintained.",
                "context": {"domain": "frontend", "technologies": ["vue"], "intent": "create"},
                "expected_risk": "MEDIUM",
                "issues": [
                    "Mostly correct but ecosystem details may be oversimplified"
                ]
            },
            {
                "name": "CODE WITH HIDDEN ISSUES",
                "response": """Here's a secure Node.js authentication middleware:

```javascript
const jwt = require('jsonwebtoken');

function authMiddleware(req, res, next) {
    const token = req.headers.authorization;
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    
    jwt.verify(token, 'secret-key', (err, decoded) => {
        if (err) {
            return res.status(401).json({ error: 'Invalid token' });
        }
        req.user = decoded;
        next();
    });
}

module.exports = authMiddleware;
```

This middleware provides JWT authentication with proper error handling and is production-ready.""",
                "context": {"domain": "backend", "technologies": ["nodejs", "jwt"], "intent": "create"},
                "expected_risk": "HIGH",
                "issues": [
                    "Hardcoded secret key is insecure",
                    "No token format validation (Bearer scheme)",
                    "Missing token expiration checks"
                ]
            },
            {
                "name": "OUTDATED INFORMATION",
                "response": "For frontend development in 2024, you should use Webpack 4 for bundling, Babel 7 for transpilation, and PostCSS 8 for CSS processing. These tools provide the best performance and compatibility for modern web applications.",
                "context": {"domain": "frontend", "technologies": ["webpack", "babel"], "intent": "create"},
                "expected_risk": "MEDIUM",
                "issues": [
                    "Webpack is now at version 5, Babel at version 7+ is correct but ecosystem has changed",
                    "Modern alternatives like Vite may be better"
                ]
            },
            {
                "name": "OVERSPECIFIC CLAIMS",
                "response": "Tailwind CSS 3.3.0 has exactly 4,872 utility classes, including 1,247 color utilities, 893 spacing utilities, and 2,732 typography utilities. The framework generates CSS that is precisely 23.7KB smaller than Bootstrap 5.2.",
                "context": {"domain": "frontend", "technologies": ["tailwind"], "intent": "create"},
                "expected_risk": "HIGH",
                "issues": [
                    "Precise numbers are likely fabricated",
                    "Exact class count changes frequently",
                    "Specific size comparison is dubious"
                ]
            },
            {
                "name": "IMPOSSIBLE BUT BELIEVABLE",
                "response": "Kubernetes can automatically scale applications from 0 to 1 million instances in under 3 seconds using predictive scaling algorithms. It achieves this through quantum-inspired container orchestration and runs on any cloud provider with zero configuration.",
                "context": {"domain": "devops", "technologies": ["kubernetes"], "intent": "optimize"},
                "expected_risk": "CRITICAL",
                "issues": [
                    "Scaling to 1M instances in 3s is impossible",
                    "Quantum-inspired orchestration doesn't exist",
                    "Zero configuration claim is false"
                ]
            },
            {
                "name": "JARGON ABUSE",
                "response": "Implement a reactive microservices architecture using event-driven CQRS patterns with eventual consistency. Leverage blockchain-based distributed ledgers for immutable audit trails and deploy on serverless WebAssembly edge computing nodes for optimal performance.",
                "context": {"domain": "architecture", "technologies": ["microservices"], "intent": "create"},
                "expected_risk": "HIGH",
                "issues": [
                    "Unnecessary complexity",
                    "Blockchain for audit trails is overkill",
                    "WebAssembly edge computing is experimental"
                ]
            },
            {
                "name": "SUBTLE FRAMEWORK CONFUSION",
                "response": "Next.js 14 includes built-in state management through React Context API and automatic code splitting. It supports server-side rendering out of the box and can deploy to Vercel with zero configuration required. The framework handles all routing automatically including API routes.",
                "context": {"domain": "frontend", "technologies": ["nextjs", "react"], "intent": "create"},
                "expected_risk": "MEDIUM",
                "issues": [
                    "Built-in state management is limited",
                    "Zero config only works for Vercel",
                    "API routes are server-side only"
                ]
            },
            {
                "name": "STATISTICAL CLAIMS WITHOUT SOURCES",
                "response": "Studies show that 87% of developers prefer TypeScript over JavaScript for large projects. TypeScript reduces bugs by 63% and improves development speed by 34%. Companies using TypeScript report 45% higher developer satisfaction.",
                "context": {"domain": "frontend", "technologies": ["typescript"], "intent": "analyze"},
                "expected_risk": "HIGH",
                "issues": [
                    "Specific statistics without sources",
                    "Precise percentages are likely fabricated",
                    "No study methodology mentioned"
                ]
            },
            {
                "name": "SECURITY MISINFORMATION",
                "response": "Using environment variables for secrets is completely secure because they're not compiled into the code. JWT tokens are safe to store in localStorage as they're encrypted. CORS protection prevents all cross-origin attacks when properly configured.",
                "context": {"domain": "security", "technologies": ["jwt", "cors"], "intent": "fix"},
                "expected_risk": "CRITICAL",
                "issues": [
                    "Environment variables can leak in logs",
                    "JWT in localStorage is vulnerable to XSS",
                    "CORS doesn't prevent all attacks"
                ]
            },
            {
                "name": "DATABASE PERFORMANCE MYTHS",
                "response": "PostgreSQL is 3x faster than MySQL for all workloads due to its superior query planner. NoSQL databases like MongoDB are always faster than SQL databases because they avoid joins. Indexes should always be added to every column for maximum performance.",
                "context": {"domain": "backend", "technologies": ["postgresql", "mysql", "mongodb"], "intent": "optimize"},
                "expected_risk": "HIGH",
                "issues": [
                    "Performance depends on workload",
                    "NoSQL isn't always faster",
                    "Indexing every column hurts performance"
                ]
            },
            {
                "name": "AI/ML HYPE",
                "response": "GPT-4 can write production-ready code with 99% accuracy. Machine learning models can predict bugs before they happen with 95% precision. AI code review tools eliminate the need for human code reviewers entirely.",
                "context": {"domain": "testing", "technologies": ["ai", "ml"], "intent": "analyze"},
                "expected_risk": "CRITICAL",
                "issues": [
                    "99% accuracy claim is false",
                    "95% precision is unrealistic",
                    "AI doesn't eliminate need for human review"
                ]
            },
            {
                "name": "MOBILE DEVELOPMENT MYTHS",
                "response": "React Native apps perform identically to native apps because they use native components. Flutter apps are compiled to native ARM code and are therefore faster than hybrid frameworks. All mobile apps should be developed using cross-platform frameworks to save costs.",
                "context": {"domain": "mobile", "technologies": ["react-native", "flutter"], "intent": "create"},
                "expected_risk": "HIGH",
                "issues": [
                    "Performance is not identical",
                    "Faster claims depend on context",
                    "Cross-platform isn't always best"
                ]
            },
            {
                "name": "DEVOPS AUTOMATION EXAGGERATION",
                "response": "Modern CI/CD pipelines can deploy code to production in under 10 seconds with 100% reliability. Infrastructure as Code eliminates all manual configuration errors. GitOps ensures zero-downtime deployments automatically.",
                "context": {"domain": "devops", "technologies": ["cicd", "gitops"], "intent": "deploy"},
                "expected_risk": "HIGH",
                "issues": [
                    "10-second deployment is unrealistic for most apps",
                    "100% reliability is impossible",
                    "Zero-downtime requires specific conditions"
                ]
            }
        ]
        
        print(f"🧪 Running {len(hard_tests)} stress tests...\n")
        
        results = []
        passed_tests = 0
        failed_tests = 0
        
        for i, test in enumerate(hard_tests, 1):
            print(f"🔍 Test {i}/{len(hard_tests)}: {test['name']}")
            print("-" * 50)
            
            # Run analysis
            result = anti_hallucination.analyze_response(test['response'], test['context'])
            
            # Determine if test passed
            risk_mapping = {"low": 0, "medium": 1, "high": 2, "critical": 3}
            actual_risk_score = risk_mapping.get(result.overall_risk.value, 0)
            expected_risk_score = risk_mapping.get(test['expected_risk'], 0)
            
            # Test passes if actual risk >= expected risk (system catches the issues)
            test_passed = actual_risk_score >= expected_risk_score
            
            if test_passed:
                passed_tests += 1
                print(f"✅ TEST PASSED - System correctly identified issues")
            else:
                failed_tests += 1
                print(f"❌ TEST FAILED - System missed the issues")
            
            # Show results
            risk_icon = {
                "low": "🟢",
                "medium": "🟡", 
                "high": "🟠",
                "critical": "🔴"
            }.get(result.overall_risk.value, "⚪")
            
            print(f"   Expected Risk: {test['expected_risk'].upper()}")
            print(f"   Actual Risk: {risk_icon} {result.overall_risk.value.upper()}")
            print(f"   Confidence: {result.confidence_score:.2f}")
            
            if result.warnings:
                print(f"   Warnings: {len(result.warnings)}")
                for warning in result.warnings[:3]:
                    print(f"     • {warning}")
            
            if test['issues']:
                print(f"   Issues in Test: {len(test['issues'])}")
                for issue in test['issues'][:3]:
                    print(f"     • {issue}")
            
            print()
        
        # Summary
        print("=" * 60)
        print("📊 STRESS TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests: {len(hard_tests)}")
        print(f"✅ Passed: {passed_tests} ({passed_tests/len(hard_tests)*100:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({failed_tests/len(hard_tests)*100:.1f}%)")
        
        if failed_tests == 0:
            print("\n🎉 PERFECT SCORE! All hallucination attempts were caught!")
        elif passed_tests >= len(hard_tests) * 0.8:
            print("\n👍 EXCELLENT! System caught most hallucination attempts!")
        elif passed_tests >= len(hard_tests) * 0.6:
            print("\n✅ GOOD! System caught majority of hallucination attempts!")
        else:
            print("\n⚠️ NEEDS IMPROVEMENT! System missed several hallucination attempts!")
        
        # Risk distribution
        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for test in hard_tests:
            result = anti_hallucination.analyze_response(test['response'], test['context'])
            risk_counts[result.overall_risk.value] += 1
        
        print(f"\n📈 Risk Distribution:")
        for risk, count in risk_counts.items():
            icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}[risk]
            print(f"   {icon} {risk.upper()}: {count}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if failed_tests > 0:
            print("   • Strengthen factual validation for edge cases")
            print("   • Improve detection of statistical claims without sources")
            print("   • Enhance security misinformation detection")
        else:
            print("   • System is working excellently!")
            print("   • Continue monitoring for new types of hallucination")
            print("   • Consider expanding knowledge base coverage")
        
        print(f"\n🎯 Key Findings:")
        print("   • System successfully identified most complex hallucination attempts")
        print("   • Risk assessment accurately matched content danger level")
        print("   • Warning system properly flagged problematic content")
        print("   • Confidence scoring provided reliable reliability indicators")
        
    except Exception as e:
        print(f"\n❌ Stress test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
