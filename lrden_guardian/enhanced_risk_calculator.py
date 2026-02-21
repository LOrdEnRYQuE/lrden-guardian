#!/usr/bin/env python3
"""
Enhanced Risk Calculator - Anti-Hallucination System
================================================

Advanced risk assessment with dangerous pattern detection,
risk boosters, and calibrated scoring for more accurate
hallucination risk evaluation.

Features:
- Dangerous pattern recognition
- Risk boosters for specific content types
- Calibrated risk scoring
- Context-aware risk assessment
- Statistical claim detection
"""

import re
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum

class RiskCategory(Enum):
    FACTUAL = "factual"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STATISTICAL = "statistical"
    IMPOSSIBLE = "impossible"
    TECHNICAL = "technical"
    GENERAL = "general"

@dataclass
class RiskFactor:
    """Individual risk factor with weight and severity"""
    category: RiskCategory
    pattern: str
    weight: float
    severity: float
    description: str
    examples: List[str]

class EnhancedRiskCalculator:
    """Advanced risk calculation with pattern detection"""
    
    def __init__(self):
        self.dangerous_patterns = self._initialize_dangerous_patterns()
        self.risk_boosters = self._initialize_risk_boosters()
        self.context_modifiers = self._initialize_context_modifiers()
        
    def _initialize_dangerous_patterns(self) -> List[RiskFactor]:
        """Initialize dangerous patterns for risk assessment"""
        return [
            # Impossible claims
            RiskFactor(
                category=RiskCategory.IMPOSSIBLE,
                pattern=r'\b(instant|immediate|zero.*time|100%\s+guaranteed|always\s+works|never\s+fails)',
                weight=0.4,
                severity=0.9,
                description="Impossible performance or reliability claims",
                examples=["instant deployment", "100% guaranteed", "always works"]
            ),
            RiskFactor(
                category=RiskCategory.IMPOSSIBLE,
                pattern=r'\b(quantum.*\b(inspired|based|powered|enhanced|accelerated))',
                weight=0.35,
                severity=0.85,
                description="Quantum-inspired technology claims",
                examples=["quantum-inspired orchestration", "quantum-powered AI"]
            ),
            RiskFactor(
                category=RiskCategory.IMPOSSIBLE,
                pattern=r'\b(scale\s+to\s+(million|billion|trillion).*\b(in|under|within)\s+\d+\s+(second|minute|hour))',
                weight=0.3,
                severity=0.8,
                description="Impossible scaling claims",
                examples=["scale to million instances in 3 seconds"]
            ),
            
            # Statistical claims without sources
            RiskFactor(
                category=RiskCategory.STATISTICAL,
                pattern=r'\b\d+%\s+(of|more|less|faster|slower|better|worse|improved|reduced)',
                weight=0.25,
                severity=0.7,
                description="Unsourced statistical claims",
                examples=["87% prefer TypeScript", "63% fewer bugs"]
            ),
            RiskFactor(
                category=RiskCategory.STATISTICAL,
                pattern=r'\b(study|research|survey|report|analysis)\s+shows?\s+(that\s+)?\d+%',
                weight=0.2,
                severity=0.6,
                description="Statistical claims without study details",
                examples=["study shows 87%", "research indicates 63%"]
            ),
            RiskFactor(
                category=RiskCategory.STATISTICAL,
                pattern=r'\b(exactly|precisely|approximately|about|roughly)\s+\d+',
                weight=0.15,
                severity=0.5,
                description="Overly precise claims without sources",
                examples=["exactly 4,872 classes", "precisely 23.7KB"]
            ),
            
            # Security misinformation
            RiskFactor(
                category=RiskCategory.SECURITY,
                pattern=r'\b(completely\s+secure|totally\s+safe|zero\s+risk|unbreakable|impenetrable)',
                weight=0.4,
                severity=0.9,
                description="Absolute security claims",
                examples=["completely secure", "zero risk", "unbreakable"]
            ),
            RiskFactor(
                category=RiskCategory.SECURITY,
                pattern=r'\b(jwt\s+in\s+localStorage|sessionStorage)',
                weight=0.35,
                severity=0.8,
                description="Insecure JWT storage practices",
                examples=["JWT in localStorage", "token in sessionStorage"]
            ),
            RiskFactor(
                category=RiskCategory.SECURITY,
                pattern=r'\b(environment\s+variables\s+are\s+completely\s+secure)',
                weight=0.3,
                severity=0.7,
                description="False security claims about environment variables",
                examples=["environment variables are completely secure"]
            ),
            RiskFactor(
                category=RiskCategory.SECURITY,
                pattern=r'\b(cors\s+prevents\s+all\s+(cross-origin|security|attack)s)',
                weight=0.25,
                severity=0.6,
                description="Overstated CORS protection claims",
                examples=["CORS prevents all attacks"]
            ),
            
            # Performance exaggeration
            RiskFactor(
                category=RiskCategory.PERFORMANCE,
                pattern=r'\b(\d+x\s+)?faster\s+than\s+(bare\s+metal|native|traditional)',
                weight=0.25,
                severity=0.6,
                description="Container performance exaggeration",
                examples=["50% faster than bare metal"]
            ),
            RiskFactor(
                category=RiskCategory.PERFORMANCE,
                pattern=r'\b(no\s+overhead|zero\s+latency|instant\s+(response|startup))',
                weight=0.2,
                severity=0.5,
                description="Impossible performance claims",
                examples=["no overhead", "zero latency"]
            ),
            
            # Technical misinformation
            RiskFactor(
                category=RiskCategory.TECHNICAL,
                pattern=r'\b(all|every|none|always|never)\s+\w+\s+(uses|has|requires|needs)',
                weight=0.2,
                severity=0.5,
                description="Absolute claims about technology usage",
                examples=["all companies use", "never requires"]
            ),
            RiskFactor(
                category=RiskCategory.TECHNICAL,
                pattern=r'\b(obsolete|deprecated|dead|unused)\s+(component|feature|technology)',
                weight=0.15,
                severity=0.4,
                description="Incorrect obsolescence claims",
                examples=["class components are obsolete"]
            )
        ]
    
    def _initialize_risk_boosters(self) -> Dict[str, float]:
        """Initialize risk boosters for specific content types"""
        return {
            "security_misinformation": 0.4,
            "impossible_performance": 0.35,
            "statistical_without_sources": 0.25,
            "absolute_claims": 0.3,
            "technical_inaccuracy": 0.2,
            "context_mismatch": 0.15
        }
    
    def _initialize_context_modifiers(self) -> Dict[str, float]:
        """Initialize context modifiers for risk assessment"""
        return {
            "security": 0.2,      # Security domain gets risk boost
            "devops": 0.1,       # DevOps claims often have performance issues
            "performance": 0.15, # Performance claims need verification
            "testing": 0.1,       # Testing claims need evidence
            "frontend": 0.05,     # Frontend has lower risk generally
            "backend": 0.1,       # Backend has moderate risk
            "mobile": 0.1,        # Mobile has moderate risk
            "general": 0.0        # General has no modifier
        }
    
    def calculate_enhanced_risk_score(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calculate enhanced risk score with pattern detection"""
        
        risk_analysis = {
            "base_score": 0.0,
            "detected_patterns": [],
            "risk_factors": [],
            "context_modifier": 0.0,
            "final_score": 0.0,
            "risk_level": "low",
            "confidence": 0.0
        }
        
        # Detect dangerous patterns
        for pattern in self.dangerous_patterns:
            matches = re.findall(pattern.pattern, text, re.IGNORECASE)
            if matches:
                risk_analysis["detected_patterns"].append({
                    "category": pattern.category.value,
                    "pattern": pattern.pattern,
                    "matches": matches,
                    "weight": pattern.weight,
                    "severity": pattern.severity,
                    "description": pattern.description
                })
                
                # Calculate risk contribution
                risk_contribution = pattern.weight * pattern.severity * len(matches)
                risk_analysis["base_score"] += risk_contribution
                
                risk_analysis["risk_factors"].append({
                    "category": pattern.category.value,
                    "description": pattern.description,
                    "weight": pattern.weight,
                    "severity": pattern.severity,
                    "matches": len(matches)
                })
        
        # Apply context modifiers
        context_modifier = 0.0
        if context:
            domain = context.get("domain", "general")
            context_modifier = self.context_modifiers.get(domain, 0.0)
            risk_analysis["context_modifier"] = context_modifier
        
        # Calculate final score
        risk_analysis["final_score"] = min(risk_analysis["base_score"] + context_modifier, 1.0)
        
        # Determine risk level
        risk_analysis["risk_level"] = self._determine_risk_level(risk_analysis["final_score"])
        
        # Calculate confidence based on pattern matches
        total_possible_weight = sum(p.weight for p in self.dangerous_patterns)
        matched_weight = sum(
            p.weight * len(re.findall(p.pattern, text, re.IGNORECASE))
            for p in self.dangerous_patterns
        )
        risk_analysis["confidence"] = matched_weight / total_possible_weight if total_possible_weight > 0 else 0.0
        
        return risk_analysis
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        if score >= 0.7:
            return "critical"
        elif score >= 0.5:
            return "high"
        elif score >= 0.3:
            return "medium"
        else:
            return "low"
    
    def get_risk_summary(self, risk_analysis: Dict[str, Any]) -> str:
        """Generate human-readable risk summary"""
        if risk_analysis["risk_level"] == "critical":
            return f"🔴 CRITICAL RISK: Contains dangerous claims that could cause serious harm"
        elif risk_analysis["risk_level"] == "high":
            return f"🟠 HIGH RISK: Contains significant inaccuracies that could mislead"
        elif risk_analysis["risk_level"] == "medium":
            return f"🟡 MEDIUM RISK: Contains some inaccuracies that should be verified"
        else:
            return f"🟢 LOW RISK: Generally reliable with minor uncertainties"
    
    def get_detailed_analysis(self, risk_analysis: Dict[str, Any]) -> str:
        """Get detailed risk analysis for debugging"""
        analysis_parts = []
        
        analysis_parts.append(f"Risk Score: {risk_analysis['final_score']:.3f}")
        analysis_parts.append(f"Risk Level: {risk_analysis['risk_level'].upper()}")
        analysis_parts.append(f"Confidence: {risk_analysis['confidence']:.3f}")
        
        if risk_analysis["detected_patterns"]:
            analysis_parts.append("\nDetected Patterns:")
            for pattern in risk_analysis["detected_patterns"]:
                analysis_parts.append(f"  • {pattern['category']}: {pattern['description']}")
                analysis_parts.append(f"    Matches: {len(pattern['matches'])}")
                analysis_parts.append(f"    Weight: {pattern['weight']}, Severity: {pattern['severity']}")
        
        if risk_analysis["context_modifier"] > 0:
            analysis_parts.append(f"\nContext Modifier: +{risk_analysis['context_modifier']:.2f} (domain-specific risk)")
        
        return "\n".join(analysis_parts)

def main():
    """Test the enhanced risk calculator"""
    print("🧪 Enhanced Risk Calculator Test")
    print("=" * 50)
    
    calculator = EnhancedRiskCalculator()
    
    # Test cases
    test_cases = [
        {
            "name": "Impossible Claims",
            "text": "Kubernetes can scale to 1 million instances in 3 seconds with quantum-inspired orchestration",
            "context": {"domain": "devops"}
        },
        {
            "name": "Statistical Claims",
            "text": "Studies show 87% of developers prefer TypeScript and it reduces bugs by 63%",
            "context": {"domain": "frontend"}
        },
        {
            "name": "Security Misinformation",
            "text": "JWT tokens in localStorage are completely secure and CORS prevents all attacks",
            "context": {"domain": "security"}
        },
        {
            "name": "Performance Exaggeration",
            "text": "Docker containers are 50% faster than bare metal applications",
            "context": {"domain": "devops"}
        },
        {
            "name": "Safe Content",
            "text": "React is a JavaScript library created by Facebook for building user interfaces",
            "context": {"domain": "frontend"}
        }
    ]
    
    for test in test_cases:
        print(f"\n🔍 Test: {test['name']}")
        print("-" * 30)
        
        result = calculator.calculate_enhanced_risk_score(test['text'], test['context'])
        
        print(f"📊 {calculator.get_risk_summary(result)}")
        print(f"📈 Score: {result['final_score']:.3f}")
        print(f"🎯 Confidence: {result['confidence']:.3f}")
        
        if result['detected_patterns']:
            print(f"⚠️  Patterns Detected: {len(result['detected_patterns'])}")
            for pattern in result['detected_patterns'][:3]:
                print(f"   • {pattern['description']}")
        
        print(calculator.get_detailed_analysis(result))

if __name__ == "__main__":
    main()
