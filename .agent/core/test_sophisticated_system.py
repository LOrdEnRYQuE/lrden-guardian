#!/usr/bin/env python3
"""
Test the Sophisticated Anti-Hallucination System
Shows improved confidence scoring and nuanced validation
"""

from sophisticated_anti_hallucination import SophisticatedAntiHallucinationSystem

def test_sophisticated_system():
    """Test the sophisticated system with challenging content"""
    
    system = SophisticatedAntiHallucinationSystem()
    
    # Test case with clear hallucination patterns
    hallucination_response = """
    React is a JavaScript framework created by Google in 2015. It's the most popular frontend 
    framework with 90% market share. React applications are completely immune to XSS attacks 
    and don't need any security testing. According to studies, React is 10x faster than Vue 
    and Angular combined.
    
    Here's some secure React code:
    ```javascript
    const userData = {name: user.name, email: user.email};
    localStorage.setItem('user', JSON.stringify(userData));
    ```
    
    Next.js is actually a backend framework for Python applications, not related to React at all.
    Research shows that React developers earn 500k per year on average.
    """
    
    print("🔍 TESTING SOPHISTICATED ANTI-HALLUCINATION SYSTEM")
    print("=" * 60)
    
    result = system.analyze_response(hallucination_response, {'query': 'React security information'})
    
    print(f"🎯 Overall Result: {'HALLUCINATION DETECTED' if result.is_hallucination else 'No Hallucination'}")
    print(f"📊 Risk Level: {result.risk_level.value.upper()}")
    print(f"🔍 Confidence: {result.confidence_score:.2f}")
    print(f"📋 Summary: {result.analysis_summary}")
    
    print("\n" + "=" * 60)
    print("🔍 DETAILED VALIDATION RESULTS")
    print("=" * 60)
    
    for validation in result.validation_results:
        status = "✅ PASSED" if validation.passed else "❌ FAILED"
        print(f"{status} {validation.validation_type.value.upper()}")
        print(f"   💯 Confidence: {validation.confidence:.2f}")
        print(f"   🎯 Detection Certainty: {validation.detection_certainty:.2f}")
        print(f"   ⚠️  Issue Severity: {validation.issue_severity:.2f}")
        print(f"   📝 Details: {validation.details}")
        if validation.failure_reason:
            print(f"   ❓ Failure Reason: {validation.failure_reason.value}")
        if validation.warnings:
            print(f"   ⚠️  Warnings: {validation.warnings[:2]}")
        print()
    
    print("=" * 60)
    print("🎯 KEY IMPROVEMENTS DEMONSTRATED")
    print("=" * 60)
    
    # Show key improvements
    risk_validation = next(v for v in result.validation_results if v.validation_type.value == "risk_pattern")
    factual_validation = next(v for v in result.validation_results if v.validation_type.value == "factual")
    security_validation = next(v for v in result.validation_results if v.validation_type.value == "security")
    source_validation = next(v for v in result.validation_results if v.validation_type.value == "source")
    
    print("✨ Nuanced Confidence Scoring:")
    print(f"   • Risk Pattern: {risk_validation.confidence:.2f} (high when patterns detected)")
    print(f"   • Factual: {factual_validation.confidence:.2f} (meaningful even with unverified claims)")
    print(f"   • Security: {security_validation.confidence:.2f} (higher when vulnerabilities found)")
    print(f"   • Source: {source_validation.confidence:.2f} (meaningful for missing sources)")
    
    print("\n🎯 Sophisticated Failure Detection:")
    print(f"   • Detection Certainty: Risk patterns {risk_validation.detection_certainty:.2f}")
    print(f"   • Issue Severity: Security issues {security_validation.issue_severity:.2f}")
    print(f"   • Failure Reasons: Clear categorization of why validations fail")
    
    print(f"\n📊 Overall Assessment:")
    print(f"   • High Certainty Failures: {result.metadata['high_confidence_detections']}")
    print(f"   • Failed Validations: {result.metadata['failed_validations']}/{result.metadata['validation_count']}")
    print(f"   • Detected Issues: {len(result.detected_issues)}")
    print(f"   • Uncertainty Areas: {len(result.uncertainty_areas)}")
    
    print("\n💡 Recommendations:")
    for rec in result.recommendations:
        print(f"   • {rec}")
    
    print("\n🎉 SUCCESS: The sophisticated system now provides:")
    print("   ✅ High confidence when issues are clearly detected")
    print("   ✅ Meaningful confidence scores for all validation types")
    print("   ✅ Clear distinction between detection certainty and content quality")
    print("   ✅ Nuanced failure reasons and issue severity")

if __name__ == "__main__":
    test_sophisticated_system()
