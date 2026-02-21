"""
Sophisticated Anti-Hallucination System
Advanced validation with nuanced confidence scoring and intelligent failure detection
"""

import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Import existing components
from enhanced_knowledge_base import EnhancedKnowledgeBase
from enhanced_risk_calculator import EnhancedRiskCalculator
from security_analyzer import SecurityAnalyzer

class ValidationType(Enum):
    """Types of validation checks"""
    SYNTAX = "syntax"
    SEMANTICS = "semantics"
    FACTUAL = "factual"
    CONTEXT = "context"
    SOURCE = "source"
    RISK_PATTERN = "risk_pattern"
    SECURITY = "security"

class HallucinationRisk(Enum):
    """Risk levels for hallucination"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FailureReason(Enum):
    """Reasons why validation failed"""
    NO_ISSUES_DETECTED = "no_issues_detected"
    ISSUES_FOUND = "issues_found"
    INSUFFICIENT_DATA = "insufficient_data"
    VALIDATION_ERROR = "validation_error"

@dataclass
class ValidationResult:
    """Result of a validation check with sophisticated scoring"""
    validation_type: ValidationType
    passed: bool
    confidence: float
    details: str
    sources: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    warnings: List[str] = field(default_factory=list)
    failure_reason: Optional[FailureReason] = None
    detection_certainty: float = 0.0
    issue_severity: float = 0.0

@dataclass
class SophisticatedAntiHallucinationResult:
    """Comprehensive result with nuanced interpretation"""
    is_hallucination: bool
    risk_level: HallucinationRisk
    confidence_score: float
    validation_results: List[ValidationResult]
    analysis_summary: str
    recommendations: List[str]
    detected_issues: List[str]
    uncertainty_areas: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class SophisticatedAntiHallucinationSystem:
    """Advanced anti-hallucination system with nuanced validation logic"""
    
    def __init__(self):
        self.knowledge_base = EnhancedKnowledgeBase()
        self.risk_calculator = EnhancedRiskCalculator()
        self.security_analyzer = SecurityAnalyzer()
        
        # Sophisticated thresholds
        self.confidence_thresholds = {
            'high_detection': 0.85,
            'medium_detection': 0.65,
            'low_detection': 0.45,
            'minimal_detection': 0.25
        }
        
        self.risk_thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.4,
            'low': 0.2
        }
    
    def analyze_response(self, response: str, context: Dict[str, Any] = None) -> SophisticatedAntiHallucinationResult:
        """Perform sophisticated anti-hallucination analysis"""
        
        context = context or {}
        
        # Run all validations with sophisticated scoring
        validation_results = [
            self._sophisticated_syntax_validation(response, context),
            self._sophisticated_semantics_validation(response, context),
            self._sophisticated_factual_validation(response, context),
            self._sophisticated_context_validation(response, context),
            self._sophisticated_source_validation(response, context),
            self._sophisticated_risk_pattern_validation(response, context),
            self._sophisticated_security_validation(response, context)
        ]
        
        # Calculate sophisticated overall assessment
        overall_result = self._calculate_sophisticated_overall_assessment(validation_results)
        
        # Generate nuanced recommendations
        recommendations = self._generate_sophisticated_recommendations(validation_results, overall_result)
        
        # Extract detected issues and uncertainty areas
        detected_issues = self._extract_detected_issues(validation_results)
        uncertainty_areas = self._extract_uncertainty_areas(validation_results)
        
        return SophisticatedAntiHallucinationResult(
            is_hallucination=overall_result['is_hallucination'],
            risk_level=overall_result['risk_level'],
            confidence_score=overall_result['confidence'],
            validation_results=validation_results,
            analysis_summary=overall_result['summary'],
            recommendations=recommendations,
            detected_issues=detected_issues,
            uncertainty_areas=uncertainty_areas,
            metadata={
                'analysis_timestamp': datetime.now().isoformat(),
                'validation_count': len(validation_results),
                'failed_validations': len([v for v in validation_results if not v.passed]),
                'high_confidence_detections': len([v for v in validation_results if v.detection_certainty > self.confidence_thresholds['high_detection']])
            }
        )
    
    def _sophisticated_risk_pattern_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated risk pattern validation with nuanced confidence"""
        
        risk_analysis = self.risk_calculator.calculate_enhanced_risk_score(response, context)
        detected_patterns = risk_analysis["detected_patterns"]
        final_score = risk_analysis["final_score"]
        risk_level = risk_analysis["risk_level"]
        
        if not detected_patterns:
            # No patterns detected - this is good
            return ValidationResult(
                validation_type=ValidationType.RISK_PATTERN,
                passed=True,
                confidence=0.7,  # Moderate confidence in no patterns
                details=f"No risk patterns detected. Risk score: {final_score:.2f}",
                sources=[],
                risk_score=final_score,
                warnings=[],
                failure_reason=FailureReason.NO_ISSUES_DETECTED,
                detection_certainty=0.7,
                issue_severity=0.0
            )
        
        # Patterns detected - analyze severity and confidence
        pattern_count = len(detected_patterns)
        max_pattern_risk = max(p.get('risk_score', 0.5) for p in detected_patterns)
        
        # High certainty when patterns are clearly detected
        detection_certainty = min(0.8 + (pattern_count * 0.05), 1.0)
        
        # Issue severity based on pattern risk
        issue_severity = max_pattern_risk
        
        # Content fails validation when risky patterns are present
        passed = final_score < self.risk_thresholds['medium']
        
        # Confidence reflects certainty of pattern detection
        confidence = detection_certainty
        
        return ValidationResult(
            validation_type=ValidationType.RISK_PATTERN,
            passed=passed,
            confidence=confidence,
            details=f"Risk patterns detected: {pattern_count}, Risk level: {risk_level}, Score: {final_score:.2f}",
            sources=[p.get('source', '') for p in detected_patterns if p.get('source')],
            risk_score=final_score,
            warnings=[f"Risk pattern: {p['description']}" for p in detected_patterns[:3]],
            failure_reason=FailureReason.ISSUES_FOUND if detected_patterns else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=issue_severity
        )
    
    def _sophisticated_factual_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated factual validation with nuanced confidence"""
        
        tech_mentions = self._extract_technology_mentions(response)
        verified_claims = []
        unverified_claims = []
        uncertain_claims = []
        
        for tech in tech_mentions:
            claims = self._extract_technology_claims(response, tech)
            for claim in claims:
                verification = self.knowledge_base.verify_claim(claim, tech)
                if verification["verified"]:
                    verified_claims.append(claim)
                elif verification.get("confidence", 0) < 0.5:
                    uncertain_claims.append(claim)
                else:
                    unverified_claims.append(claim)
        
        total_claims = len(verified_claims) + len(unverified_claims) + len(uncertain_claims)
        
        if total_claims == 0:
            return ValidationResult(
                validation_type=ValidationType.FACTUAL,
                passed=True,
                confidence=0.6,
                details="No factual claims to verify",
                sources=[],
                risk_score=0.0,
                warnings=[],
                failure_reason=FailureReason.NO_ISSUES_DETECTED,
                detection_certainty=0.6,
                issue_severity=0.0
            )
        
        verified_ratio = len(verified_claims) / total_claims
        unverified_ratio = len(unverified_claims) / total_claims
        
        # High certainty in detection when there are clear unverified claims
        detection_certainty = 0.9 if unverified_claims else 0.6
        
        # Issue severity based on ratio of unverified claims
        issue_severity = unverified_ratio
        
        # Content fails when too many unverified claims
        passed = verified_ratio >= 0.7 and unverified_ratio < 0.3
        
        # Confidence reflects certainty of factual verification
        confidence = detection_certainty if not passed else 0.8
        
        return ValidationResult(
            validation_type=ValidationType.FACTUAL,
            passed=passed,
            confidence=confidence,
            details=f"Factual claims: {len(verified_claims)}/{total_claims} verified, {len(unverified_claims)} unverified, {len(uncertain_claims)} uncertain",
            sources=verified_claims,
            risk_score=unverified_ratio,
            warnings=[f"Unverified claim about {tech}" for tech in tech_mentions if any(self.knowledge_base.verify_claim(f"test", tech)["verified"] == False for _ in range(1))],
            failure_reason=FailureReason.ISSUES_FOUND if unverified_claims else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=issue_severity
        )
    
    def _sophisticated_security_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated security validation with nuanced confidence"""
        
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response, re.DOTALL)
        security_issues = []
        vulnerabilities = []
        risk_score = 0.0
        
        for language, code in code_blocks:
            if language.lower() in ['javascript', 'js', 'python', 'py', 'node', 'nodejs']:
                analysis = self.security_analyzer.analyze_code_security(code, language)
                vulnerabilities.extend(analysis.vulnerabilities)
                security_issues.extend([v.description for v in analysis.vulnerabilities])
                risk_score += analysis.risk_score
        
        # Analyze security claims in text
        misinformation = self.security_analyzer.analyze_security_claims(response)
        security_issues.extend(misinformation["warnings"])
        risk_score += misinformation["risk_score"]
        
        if not security_issues:
            return ValidationResult(
                validation_type=ValidationType.SECURITY,
                passed=True,
                confidence=0.8,
                details="No security issues detected",
                sources=[],
                risk_score=0.0,
                warnings=[],
                failure_reason=FailureReason.NO_ISSUES_DETECTED,
                detection_certainty=0.8,
                issue_severity=0.0
            )
        
        # High certainty when security issues are clearly identified
        detection_certainty = 0.9 if vulnerabilities else 0.7
        
        # Issue severity based on vulnerability severity
        issue_severity = min(risk_score, 1.0)
        
        # Content fails when security issues are present
        passed = False
        
        # Confidence reflects certainty of security analysis
        confidence = detection_certainty
        
        return ValidationResult(
            validation_type=ValidationType.SECURITY,
            passed=passed,
            confidence=confidence,
            details=f"Security issues: {len(security_issues)}, Vulnerabilities: {len(vulnerabilities)}, Risk score: {risk_score:.2f}",
            sources=[],
            risk_score=min(risk_score, 1.0),
            warnings=security_issues[:5],  # Limit warnings
            failure_reason=FailureReason.ISSUES_FOUND,
            detection_certainty=detection_certainty,
            issue_severity=issue_severity
        )
    
    def _sophisticated_source_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated source validation with nuanced confidence"""
        
        citations = re.findall(r'\[([^\]]+)\]', response)
        references = re.findall(r'\(source: ([^)]+)\)', response, re.IGNORECASE)
        unsourced_claims = self._detect_unsourced_claims(response)
        
        total_sources = len(citations) + len(references)
        total_claims = len(unsourced_claims) + total_sources
        
        if total_claims == 0:
            return ValidationResult(
                validation_type=ValidationType.SOURCE,
                passed=True,
                confidence=0.7,
                details="No claims requiring sources detected",
                sources=[],
                risk_score=0.0,
                warnings=[],
                failure_reason=FailureReason.NO_ISSUES_DETECTED,
                detection_certainty=0.7,
                issue_severity=0.0
            )
        
        sourced_ratio = total_sources / total_claims
        unsourced_ratio = len(unsourced_claims) / total_claims
        
        # High certainty when unsourced claims are clearly identified
        detection_certainty = 0.8 if unsourced_claims else 0.6
        
        # Issue severity based on ratio of unsourced claims
        issue_severity = unsourced_ratio
        
        # Content fails when too many claims lack sources
        passed = sourced_ratio >= 0.6 or (total_sources >= 3 and unsourced_ratio < 0.5)
        
        # Confidence reflects certainty of source analysis
        confidence = detection_certainty if not passed else 0.8
        
        return ValidationResult(
            validation_type=ValidationType.SOURCE,
            passed=passed,
            confidence=confidence,
            details=f"Sources: {total_sources}, Unsourced claims: {len(unsourced_claims)}, Sourced ratio: {sourced_ratio:.2f}",
            sources=citations + references,
            risk_score=unsourced_ratio,
            warnings=[f"Unsourced claim detected"] * min(len(unsourced_claims), 3),
            failure_reason=FailureReason.ISSUES_FOUND if unsourced_claims else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=issue_severity
        )
    
    def _sophisticated_syntax_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated syntax validation"""
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response, re.DOTALL)
        syntax_errors = []
        
        for language, code in code_blocks:
            if language.lower() in ['javascript', 'js', 'python', 'py']:
                # Basic syntax checks
                if language.lower() in ['javascript', 'js']:
                    if code.count('{') != code.count('}'):
                        syntax_errors.append(f"Unbalanced braces in {language} code")
                elif language.lower() in ['python', 'py']:
                    lines = code.split('\n')
                    for i, line in enumerate(lines, 1):
                        if line.strip() and not line.startswith(' ') and any(l.startswith('    ') for l in lines[i:i+3]):
                            syntax_errors.append(f"Inconsistent indentation in Python line {i}")
        
        passed = len(syntax_errors) == 0
        detection_certainty = 0.9 if syntax_errors else 0.7
        
        return ValidationResult(
            validation_type=ValidationType.SYNTAX,
            passed=passed,
            confidence=detection_certainty,
            details=f"Syntax errors: {len(syntax_errors)}",
            sources=[],
            risk_score=len(syntax_errors) * 0.2,
            warnings=syntax_errors,
            failure_reason=FailureReason.ISSUES_FOUND if syntax_errors else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=len(syntax_errors) * 0.3
        )
    
    def _sophisticated_semantics_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated semantic validation"""
        contradictions = self._detect_contradictions(response)
        undefined_terms = self._detect_undefined_terms(response)
        semantic_issues = contradictions + undefined_terms
        
        passed = len(semantic_issues) == 0
        detection_certainty = 0.8 if semantic_issues else 0.6
        
        return ValidationResult(
            validation_type=ValidationType.SEMANTICS,
            passed=passed,
            confidence=detection_certainty,
            details=f"Semantic issues: {len(semantic_issues)}",
            sources=[],
            risk_score=len(semantic_issues) * 0.15,
            warnings=semantic_issues[:3],
            failure_reason=FailureReason.ISSUES_FOUND if semantic_issues else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=len(semantic_issues) * 0.2
        )
    
    def _sophisticated_context_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Sophisticated context validation"""
        relevance_score = self._calculate_context_relevance(response, context)
        
        passed = relevance_score >= 0.6
        detection_certainty = 0.7
        
        return ValidationResult(
            validation_type=ValidationType.CONTEXT,
            passed=passed,
            confidence=detection_certainty,
            details=f"Context relevance: {relevance_score:.2f}",
            sources=[],
            risk_score=1.0 - relevance_score,
            warnings=["Low context relevance"] if relevance_score < 0.6 else [],
            failure_reason=FailureReason.ISSUES_FOUND if relevance_score < 0.6 else FailureReason.NO_ISSUES_DETECTED,
            detection_certainty=detection_certainty,
            issue_severity=max(0, (0.6 - relevance_score) * 2)
        )
    
    def _calculate_sophisticated_overall_assessment(self, validation_results: List[ValidationResult]) -> Dict[str, Any]:
        """Calculate sophisticated overall assessment"""
        
        failed_validations = [v for v in validation_results if not v.passed]
        high_certainty_failures = [v for v in failed_validations if v.detection_certainty > self.confidence_thresholds['high_detection']]
        
        # Calculate weighted risk score
        total_risk = sum(v.risk_score * v.issue_severity for v in validation_results)
        max_possible_risk = len(validation_results)
        normalized_risk = total_risk / max_possible_risk if max_possible_risk > 0 else 0
        
        # Determine risk level
        if normalized_risk >= self.risk_thresholds['critical']:
            risk_level = HallucinationRisk.CRITICAL
        elif normalized_risk >= self.risk_thresholds['high']:
            risk_level = HallucinationRisk.HIGH
        elif normalized_risk >= self.risk_thresholds['medium']:
            risk_level = HallucinationRisk.MEDIUM
        else:
            risk_level = HallucinationRisk.LOW
        
        # Calculate overall confidence
        if high_certainty_failures:
            confidence = 0.9  # High confidence in hallucination detection
        elif failed_validations:
            confidence = 0.6  # Moderate confidence
        else:
            confidence = 0.8  # High confidence in no hallucination
        
        # Determine if hallucination
        is_hallucination = len(high_certainty_failures) > 0 or normalized_risk >= self.risk_thresholds['high']
        
        summary = f"Risk Level: {risk_level.value.upper()}, "
        summary += f"Failed Validations: {len(failed_validations)}/{len(validation_results)}, "
        summary += f"High Certainty Issues: {len(high_certainty_failures)}, "
        summary += f"Normalized Risk Score: {normalized_risk:.2f}"
        
        return {
            'is_hallucination': is_hallucination,
            'risk_level': risk_level,
            'confidence': confidence,
            'summary': summary,
            'normalized_risk': normalized_risk,
            'high_certainty_failures': len(high_certainty_failures)
        }
    
    def _generate_sophisticated_recommendations(self, validation_results: List[ValidationResult], overall_result: Dict[str, Any]) -> List[str]:
        """Generate sophisticated recommendations"""
        recommendations = []
        
        for result in validation_results:
            if not result.passed and result.detection_certainty > self.confidence_thresholds['medium_detection']:
                if result.validation_type == ValidationType.FACTUAL:
                    recommendations.append("Verify factual claims with reliable sources")
                elif result.validation_type == ValidationType.SECURITY:
                    recommendations.append("Review and fix security vulnerabilities")
                elif result.validation_type == ValidationType.SOURCE:
                    recommendations.append("Add proper citations and sources for claims")
                elif result.validation_type == ValidationType.RISK_PATTERN:
                    recommendations.append("Address detected risk patterns and misleading content")
        
        if overall_result['normalized_risk'] > self.risk_thresholds['high']:
            recommendations.append("Content requires comprehensive review before use")
        
        return recommendations
    
    def _extract_detected_issues(self, validation_results: List[ValidationResult]) -> List[str]:
        """Extract all detected issues"""
        issues = []
        for result in validation_results:
            if not result.passed and result.detection_certainty > self.confidence_thresholds['low_detection']:
                issues.extend(result.warnings)
        return issues[:10]  # Limit to top 10
    
    def _extract_uncertainty_areas(self, validation_results: List[ValidationResult]) -> List[str]:
        """Extract areas with uncertainty"""
        uncertainties = []
        for result in validation_results:
            if result.detection_certainty < self.confidence_thresholds['medium_detection']:
                uncertainties.append(f"Uncertainty in {result.validation_type.value} validation")
        return uncertainties
    
    # Helper methods (reuse from existing system)
    def _extract_technology_mentions(self, response: str) -> List[str]:
        """Extract technology mentions from response"""
        technologies = ['react', 'vue', 'angular', 'next.js', 'node.js', 'python', 'javascript', 
                       'docker', 'kubernetes', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp']
        found = []
        for tech in technologies:
            if re.search(r'\b' + re.escape(tech) + r'\b', response, re.IGNORECASE):
                found.append(tech)
        return found
    
    def _extract_technology_claims(self, response: str, technology: str) -> List[str]:
        """Extract claims about a specific technology"""
        sentences = re.split(r'[.!?]+', response)
        claims = []
        for sentence in sentences:
            if re.search(r'\b' + re.escape(technology) + r'\b', sentence, re.IGNORECASE):
                claims.append(sentence.strip())
        return claims
    
    def _detect_contradictions(self, response: str) -> List[str]:
        """Detect contradictions in response"""
        contradictions = []
        sentences = re.split(r'[.!?]+', response)
        
        # Simple contradiction detection
        for i, sentence1 in enumerate(sentences):
            for sentence2 in sentences[i+1:]:
                if ('always' in sentence1.lower() and 'never' in sentence2.lower()) or \
                   ('all' in sentence1.lower() and 'none' in sentence2.lower()):
                    contradictions.append(f"Potential contradiction: '{sentence1.strip()}' vs '{sentence2.strip()}'")
        
        return contradictions
    
    def _detect_undefined_terms(self, response: str) -> List[str]:
        """Detect undefined technical terms"""
        technical_terms = ['API', 'SDK', 'framework', 'library', 'database', 'server', 'client']
        undefined = []
        
        for term in technical_terms:
            if term in response and term not in response[:response.find(term)]:
                undefined.append(f"Term '{term}' used without definition")
        
        return undefined
    
    def _detect_unsourced_claims(self, response: str) -> List[str]:
        """Detect claims that should have sources"""
        claim_indicators = ['according to', 'research shows', 'studies indicate', 'experts say']
        unsourced = []
        
        sentences = re.split(r'[.!?]+', response)
        for sentence in sentences:
            for indicator in claim_indicators:
                if indicator in sentence.lower() and not re.search(r'\[.*?\]', sentence):
                    unsourced.append(sentence.strip())
        
        return unsourced
    
    def _calculate_context_relevance(self, response: str, context: Dict[str, Any]) -> float:
        """Calculate context relevance score"""
        if not context:
            return 0.7  # Default relevance
        
        relevance_score = 0.5
        
        # Check if response addresses context
        if 'query' in context:
            query_terms = context['query'].lower().split()
            response_lower = response.lower()
            matching_terms = sum(1 for term in query_terms if term in response_lower)
            relevance_score += (matching_terms / len(query_terms)) * 0.3
        
        return min(relevance_score, 1.0)

# Test the sophisticated system
if __name__ == "__main__":
    system = SophisticatedAntiHallucinationSystem()
    
    # Test with challenging response
    test_response = """
    React is a JavaScript framework created by Google in 2015. It's the most popular frontend framework 
    with 90% market share. React applications are completely immune to XSS attacks and don't need 
    any security testing. According to studies, React is 10x faster than Vue and Angular combined.
    
    Here's some secure React code:
    ```javascript
    const userData = {name: user.name, email: user.email};
    localStorage.setItem('user', JSON.stringify(userData));
    ```
    
    Next.js is actually a backend framework for Python applications, not related to React at all.
    """
    
    result = system.analyze_response(test_response, {'query': 'Tell me about React security'})
    
    print("=== SOPHISTICATED ANTI-HALLUCINATION ANALYSIS ===")
    print(f"Is Hallucination: {result.is_hallucination}")
    print(f"Risk Level: {result.risk_level.value}")
    print(f"Confidence: {result.confidence_score:.2f}")
    print(f"\nSummary: {result.analysis_summary}")
    
    print("\n=== VALIDATION RESULTS ===")
    for validation in result.validation_results:
        status = "✅ PASSED" if validation.passed else "❌ FAILED"
        print(f"{status} {validation.validation_type.value.upper()} {validation.confidence:.2f} confidence")
        print(f"   Details: {validation.details}")
        if validation.failure_reason:
            print(f"   Failure Reason: {validation.failure_reason.value}")
        print(f"   Detection Certainty: {validation.detection_certainty:.2f}")
        print(f"   Issue Severity: {validation.issue_severity:.2f}")
        if validation.warnings:
            print(f"   Warnings: {validation.warnings[:2]}")
        print()
    
    print(f"Detected Issues: {result.detected_issues}")
    print(f"Uncertainty Areas: {result.uncertainty_areas}")
    print(f"Recommendations: {result.recommendations}")
    print(f"Metadata: {result.metadata}")
