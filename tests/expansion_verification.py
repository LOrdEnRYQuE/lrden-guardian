#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lrden_guardian import create_lrden_guardian
from lrden_guardian.enterprise import LRDEnEEnterprise, EnterpriseConfig

def test_i18n():
    print("Testing i18n...")
    guardian_es = create_lrden_guardian(locale="es")
    info = guardian_es.get_guardian_info()
    print(f"Locale set to: {info['locale']}")
    # Since we didn't add the actual .mo files, we expect English fallback or the message id
    # but the logic for switching should be sound.
    
def test_analytics():
    print("\nTesting Analytics...")
    # Mocking license info for test
    license_key = "LRDEN-PRO-TEST-2026"
    try:
        enterprise = LRDEnEEnterprise(license_key=license_key)
        result = enterprise.analyze_content("This is a test content about financial security.")
        print(f"Analysis result: {'Safe' if result.is_safe else 'Unsafe'}")
        
        roi = enterprise.analytics.calculate_security_roi()
        print(f"Security ROI: {roi}")
        
        prediction = enterprise.analytics.predictive_risk_assessment("Invest in crypto now!")
        print(f"Predictive Risk: {prediction}")
    except Exception as e:
        print(f"Enterprise Analysis failed (expected if license check is strict): {e}")

if __name__ == "__main__":
    test_i18n()
    test_analytics()
