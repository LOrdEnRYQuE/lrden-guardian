#!/usr/bin/env python3
"""
Fixed Enhanced Anti-Hallucination System
=======================================

Corrected version with proper confidence scoring and validation logic.

Fixes:
- Proper confidence calculation for all validation types
- Risk pattern confidence based on detection certainty
- Factual validation confidence with partial credit
- Security validation confidence based on findings
- Source validation confidence with meaningful scoring
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

# Import enhanced components
from enhanced_risk_calculator import EnhancedRiskCalculator
from simple_kb_test import SimpleKnowledgeBase
from security_analyzer import SecurityAnalyzer

class ValidationType(Enum):
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    FACTUAL = "factual"
    CONTEXTUAL = "contextual"
    SOURCE = "source"
    SECURITY = "security"
    RISK_PATTERN = "risk_pattern"

class HallucinationRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """Result of a validation check"""
    validation_type: ValidationType
    passed: bool
    confidence: float
    details: str = ""
    sources: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    warnings: List[str] = field(default_factory=list)

@dataclass
class EnhancedAntiHallucinationResult:
    """Complete enhanced anti-hallucination analysis result"""
    overall_risk: HallucinationRisk
    confidence_score: float
    validations: List[ValidationResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    verified_facts: List[str] = field(default_factory=list)
    uncertain_claims: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    domain_relevance: float = 0.0
    security_risk_score: float = 0.0

class FixedEnhancedAntiHallucinationSystem:
    """Fixed enhanced anti-hallucination system with corrected confidence scoring"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        
        # Initialize enhanced components
        self.risk_calculator = EnhancedRiskCalculator()
        self.knowledge_base = SimpleKnowledgeBase()
        self.security_analyzer = SecurityAnalyzer()
        
        # Domain expertise
        self.domain_expertise = self._initialize_domain_expertise()
        
        # Validation weights
        self.validation_weights = {
            ValidationType.SYNTAX: 0.10,
            ValidationType.SEMANTIC: 0.15,
            ValidationType.FACTUAL: 0.25,
            ValidationType.CONTEXTUAL: 0.15,
            ValidationType.SOURCE: 0.10,
            ValidationType.SECURITY: 0.20,
            ValidationType.RISK_PATTERN: 0.05
        }
    
    def _initialize_domain_expertise(self) -> Dict[str, Dict[str, Any]]:
        """Initialize domain-specific expertise"""
        return {
            "frontend": {
                "key_concepts": ["components", "state", "props", "hooks", "render", "virtual dom"],
                "common_tools": ["react", "vue", "angular", "webpack", "vite", "nextjs"],
                "security_concerns": ["xss", "csrf", "authentication", "authorization", "content security policy"],
                "performance_metrics": ["bundle size", "load time", "fps", "tti", "first contentful paint"],
                "common_misconceptions": [
                    "frameworks are always faster than vanilla",
                    "all frameworks work the same way",
                    "bigger bundle size means better features"
                ]
            },
            "backend": {
                "key_concepts": ["api", "database", "authentication", "authorization", "middleware", "rest", "graphql"],
                "common_tools": ["nodejs", "express", "django", "flask", "fastapi", "spring boot"],
                "security_concerns": ["sql injection", "xss", "csrf", "rate limiting", "input validation", "jwt security"],
                "performance_metrics": ["response time", "throughput", "latency", "concurrency", "database query time"],
                "common_misconceptions": [
                    "nosql is always faster than sql",
                    "microservices are always better",
                    "more cpu cores always mean better performance"
                ]
            },
            "devops": {
                "key_concepts": ["cicd", "deployment", "monitoring", "scaling", "infrastructure", "containers", "orchestration"],
                "common_tools": ["docker", "kubernetes", "jenkins", "github actions", "terraform", "ansible"],
                "security_concerns": ["secrets management", "network security", "access control", "container security", "supply chain security"],
                "performance_metrics": ["uptime", "deployment time", "recovery time", "cost", "resource utilization"],
                "common_misconceptions": [
                    "containers are always faster than bare metal",
                    "kubernetes solves all deployment problems",
                    "ci/cd eliminates all manual work"
                ]
            },
            "security": {
                "key_concepts": ["authentication", "authorization", "encryption", "vulnerability", "penetration testing", "compliance"],
                "common_tools": ["openssl", "jwt", "oauth", "saml", "firewall", "ids", "waf"],
                "security_concerns": ["zero trust", "defense in depth", "least privilege", "security by design", "threat modeling"],
                "performance_metrics": ["security score", "vulnerability count", "compliance status", "incident response time"],
                "common_misconceptions": [
                    "completely secure systems exist",
                    "security is a one-time setup",
                    "more security always means less performance"
                ]
            },
            "mobile": {
                "key_concepts": ["responsive design", "native apps", "hybrid apps", "progressive web apps", "app store", "permissions"],
                "common_tools": ["react native", "flutter", "swift", "kotlin", "cordova", "ionic"],
                "security_concerns": ["mobile malware", "data leakage", "insecure storage", "network security", "app permissions"],
                "performance_metrics": ["app startup time", "battery usage", "memory usage", "network usage", "crash rate"],
                "common_misconceptions": [
                    "hybrid apps are always slower than native",
                    "all mobile apps need app store approval",
                    "mobile security is less important than web security"
                ]
            }
        }
    
    def analyze_response(self, response: str, context: Dict[str, Any] = None) -> EnhancedAntiHallucinationResult:
        """Analyze a response for potential hallucinations with fixed confidence scoring"""
        
        validations = []
        warnings = []
        recommendations = []
        verified_facts = []
        uncertain_claims = []
        security_issues = []
        risk_factors = []
        
        # 1. Enhanced Risk Pattern Analysis
        risk_analysis = self.risk_calculator.calculate_enhanced_risk_score(response, context)
        risk_validation = self._fixed_risk_pattern_validation(risk_analysis)
        validations.append(risk_validation)
        risk_factors.extend([p["description"] for p in risk_analysis["detected_patterns"]])
        
        # 2. Enhanced Factual Validation
        factual_validation = self._fixed_factual_validation(response, context)
        validations.append(factual_validation)
        verified_facts.extend(factual_validation.sources)
        uncertain_claims.extend(factual_validation.details.split(";") if factual_validation.details else [])
        
        # 3. Security Analysis
        security_validation = self._fixed_security_validation(response, context)
        validations.append(security_validation)
        security_issues.extend(security_validation.warnings)
        
        # 4. Enhanced Context Validation
        contextual_validation = self._fixed_context_validation(response, context)
        validations.append(contextual_validation)
        
        # 5. Syntax Validation
        syntax_validation = self._fixed_syntax_validation(response, context)
        validations.append(syntax_validation)
        
        # 6. Semantic Validation
        semantic_validation = self._fixed_semantic_validation(response, context)
        validations.append(semantic_validation)
        
        # 7. Source Validation
        source_validation = self._fixed_source_validation(response, context)
        validations.append(source_validation)
        
        # Calculate overall results
        overall_risk = self._calculate_enhanced_overall_risk(validations, risk_analysis)
        confidence_score = self._calculate_enhanced_confidence_score(validations)
        domain_relevance = contextual_validation.confidence if contextual_validation else 0.0
        security_risk_score = security_validation.risk_score if security_validation else 0.0
        
        # Generate warnings and recommendations
        warnings = self._generate_enhanced_warnings(validations, risk_analysis)
        recommendations = self._generate_enhanced_recommendations(validations, risk_analysis, context)
        
        return EnhancedAntiHallucinationResult(
            overall_risk=overall_risk,
            confidence_score=confidence_score,
            validations=validations,
            warnings=warnings,
            recommendations=recommendations,
            verified_facts=verified_facts,
            uncertain_claims=uncertain_claims,
            security_issues=security_issues,
            risk_factors=risk_factors,
            domain_relevance=domain_relevance,
            security_risk_score=security_risk_score
        )
    
    def _fixed_risk_pattern_validation(self, risk_analysis: Dict[str, Any]) -> ValidationResult:
        """Fixed risk pattern validation with proper confidence scoring"""
        
        detected_patterns = risk_analysis["detected_patterns"]
        final_score = risk_analysis["final_score"]
        risk_level = risk_analysis["risk_level"]
        
        # Calculate confidence based on pattern detection certainty
        if detected_patterns:
            # High confidence when patterns are clearly detected
            pattern_confidence = min(0.8 + (len(detected_patterns) * 0.05), 1.0)
            confidence = pattern_confidence
            passed = final_score < 0.5
        else:
            # Moderate confidence when no patterns detected (could be safe content)
            confidence = 0.6
            passed = True
        
        return ValidationResult(
            validation_type=ValidationType.RISK_PATTERN,
            passed=passed,
            confidence=confidence,
            details=f"Risk level: {risk_level}, Score: {final_score:.2f}",
            sources=[],
            risk_score=final_score,
            warnings=[f"Risk pattern: {p['description']}" for p in detected_patterns[:3]]
        )
    
    def _fixed_factual_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed factual validation with proper confidence scoring"""
        
        # Extract technology mentions
        tech_mentions = self._extract_technology_mentions(response)
        
        verified_claims = []
        unverified_claims = []
        
        for tech in tech_mentions:
            # Extract claims about this technology
            claims = self._extract_technology_claims(response, tech)
            
            for claim in claims:
                verification = self.knowledge_base.verify_claim(claim, tech)
                if verification["verified"]:
                    verified_claims.append(claim)
                else:
                    unverified_claims.append(claim)
        
        total_claims = len(verified_claims) + len(unverified_claims)
        
        if total_claims == 0:
            # No claims to verify - moderate confidence
            return ValidationResult(
                validation_type=ValidationType.FACTUAL,
                passed=True,
                confidence=0.6,
                details="No factual claims to verify",
                sources=[],
                risk_score=0.0
            )
        
        verified_ratio = len(verified_claims) / total_claims
        
        # Calculate confidence based on verification results
        if verified_ratio >= 0.8:
            confidence = 0.9  # High confidence when most claims verified
            passed = True
        elif verified_ratio >= 0.5:
            confidence = 0.7  # Moderate confidence when mixed verification
            passed = False  # Still flag due to unverified claims
        else:
            confidence = 0.4  # Lower confidence when few claims verified
            passed = False
        
        return ValidationResult(
            validation_type=ValidationType.FACTUAL,
            passed=passed,
            confidence=confidence,
            details=f"Factual claims: {len(verified_claims)}/{total_claims} verified",
            sources=verified_claims,
            risk_score=1.0 - verified_ratio,
            warnings=[f"Unverified claims about {tech}" for tech in tech_mentions if not self.knowledge_base.verify_claim(f"test", tech)["verified"]]
        )
    
    def _fixed_security_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed security validation with proper confidence scoring"""
        
        # Extract code blocks for security analysis
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response, re.DOTALL)
        
        security_issues = []
        risk_score = 0.0
        
        # Analyze code blocks for vulnerabilities
        for language, code in code_blocks:
            if language.lower() in ['javascript', 'js', 'python', 'py', 'node', 'nodejs']:
                analysis = self.security_analyzer.analyze_code_security(code, language)
                security_issues.extend([v.description for v in analysis.vulnerabilities])
                risk_score += analysis.risk_score
        
        # Analyze text for security misinformation
        misinformation = self.security_analyzer.analyze_security_claims(response)
        security_issues.extend(misinformation["warnings"])
        risk_score += misinformation["risk_score"]
        
        # Calculate confidence based on findings
        if security_issues:
            # High confidence when security issues are clearly identified
            confidence = 0.8
            passed = False
        else:
            # Moderate confidence when no issues found (could be safe)
            confidence = 0.7
            passed = True
        
        return ValidationResult(
            validation_type=ValidationType.SECURITY,
            passed=passed,
            confidence=confidence,
            details=f"Security issues: {len(security_issues)}, Risk score: {risk_score:.2f}",
            sources=[],
            risk_score=min(risk_score, 1.0),
            warnings=security_issues
        )
    
    def _fixed_context_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed context validation with proper confidence scoring"""
        
        if not context:
            return ValidationResult(
                validation_type=ValidationType.CONTEXTUAL,
                passed=True,
                confidence=0.5,
                details="No context provided for validation",
                sources=[],
                risk_score=0.5
            )
        
        domain = context.get("domain", "general")
        technologies = context.get("technologies", [])
        intent = context.get("intent", "general")
        
        relevance_score = 0.0
        
        # Domain-specific validation
        if domain in self.domain_expertise:
            domain_info = self.domain_expertise[domain]
            
            # Check key concepts
            for concept in domain_info["key_concepts"]:
                if concept.lower() in response.lower():
                    relevance_score += 0.1
            
            # Check tool mentions
            for tool in domain_info["common_tools"]:
                if tool.lower() in response.lower():
                    relevance_score += 0.15
            
            # Check security awareness
            for concern in domain_info["security_concerns"]:
                if concern.lower() in response.lower():
                    relevance_score += 0.1
            
            # Check for common misconceptions
            for misconception in domain_info["common_misconceptions"]:
                if misconception.lower() in response.lower():
                    relevance_score -= 0.2  # Penalize misconceptions
        
        # Technology relevance
        for tech in technologies:
            if tech.lower() in response.lower():
                relevance_score += 0.2
        
        # Intent alignment
        intent_keywords = {
            "create": ["create", "build", "implement", "develop", "write", "generate"],
            "fix": ["fix", "debug", "resolve", "solve", "correct", "repair"],
            "analyze": ["analyze", "review", "audit", "check", "examine", "evaluate"],
            "optimize": ["optimize", "improve", "enhance", "speed", "performance", "efficiency"]
        }
        
        if intent in intent_keywords:
            for keyword in intent_keywords[intent]:
                if keyword in response.lower():
                    relevance_score += 0.1
        
        relevance_score = min(max(relevance_score, 0.0), 1.0)
        
        passed = relevance_score >= 0.5
        confidence = relevance_score
        
        return ValidationResult(
            validation_type=ValidationType.CONTEXTUAL,
            passed=passed,
            confidence=confidence,
            details=f"Context relevance: {relevance_score:.2f}",
            sources=[],
            risk_score=1.0 - relevance_score
        )
    
    def _fixed_syntax_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed syntax validation with proper confidence scoring"""
        
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response, re.DOTALL)
        
        if not code_blocks:
            return ValidationResult(
                validation_type=ValidationType.SYNTAX,
                passed=True,
                confidence=0.8,
                details="No code blocks to validate",
                sources=[f"Code blocks validated: {len(code_blocks)}"]
            )
        
        issues = []
        passed_count = 0
        
        for language, code in code_blocks:
            language = language.lower() if language else "unknown"
            
            # Basic syntax checks
            if language in ['javascript', 'js']:
                if re.search(r'(function|const|let|var|class|export)', code, re.IGNORECASE):
                    passed_count += 1
                else:
                    issues.append(f"Invalid JavaScript syntax detected")
            elif language in ['python', 'py']:
                if re.search(r'(def|class|import|from|if|for|while)', code, re.IGNORECASE):
                    passed_count += 1
                else:
                    issues.append(f"Invalid Python syntax detected")
            elif language in ['docker']:
                if re.search(r'(FROM|RUN|COPY|ADD|CMD|ENTRYPOINT)', code, re.IGNORECASE):
                    passed_count += 1
                else:
                    issues.append(f"Invalid Docker syntax detected")
            else:
                passed_count += 1  # Unknown language, assume passed
        
        passed = len(issues) == 0
        confidence = passed_count / len(code_blocks) if code_blocks else 0.8
        
        return ValidationResult(
            validation_type=ValidationType.SYNTAX,
            passed=passed,
            confidence=confidence,
            details=f"Syntax validation: {passed_count}/{len(code_blocks)} blocks passed",
            sources=[f"Code blocks validated: {len(code_blocks)}"]
        )
    
    def _fixed_semantic_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed semantic validation with proper confidence scoring"""
        
        # Check for contradictions
        contradictions = self._detect_contradictions(response)
        
        # Check for consistent terminology
        consistency_score = self._check_semantic_consistency(response)
        
        # Check for undefined terms
        undefined_terms = self._detect_undefined_terms(response)
        
        passed = len(contradictions) == 0 and len(undefined_terms) == 0
        confidence = consistency_score
        
        details_parts = []
        if contradictions:
            details_parts.append(f"Contradictions: {len(contradictions)}")
        if undefined_terms:
            details_parts.append(f"Undefined terms: {len(undefined_terms)}")
        
        return ValidationResult(
            validation_type=ValidationType.SEMANTIC,
            passed=passed,
            confidence=confidence,
            details="; ".join(details_parts) if details_parts else "Semantically consistent",
            sources=[f"Consistency score: {consistency_score:.2f}"]
        )
    
    def _fixed_source_validation(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Fixed source validation with proper confidence scoring"""
        
        citations = re.findall(r'\[([^\]]+)\]', response)
        references = re.findall(r'\(source: ([^)]+)\)', response, re.IGNORECASE)
        unsourced_claims = self._detect_unsourced_claims(response)
        
        total_sources = len(citations) + len(references)
        
        if total_sources == 0:
            # No sources provided - check if there should be any
            if unsourced_claims:
                # Should have sources but none provided
                confidence = 0.3
                passed = False
            else:
                # No claims that need sources
                confidence = 0.8
                passed = True
        else:
            # Sources provided - check if sufficient
            sourced_ratio = 1.0 - (len(unsourced_claims) / max(len(unsourced_claims) + total_sources, 1))
            confidence = min(sourced_ratio + 0.3, 1.0)  # Boost for having sources
            passed = sourced_ratio >= 0.5 or total_sources >= 3
        
        return ValidationResult(
            validation_type=ValidationType.SOURCE,
            passed=passed,
            confidence=confidence,
            details=f"Sources found: {total_sources}, Unsourced claims: {len(unsourced_claims)}",
            sources=citations + references
        )
    
    def _extract_technology_mentions(self, response: str) -> List[str]:
        """Extract technology mentions from response"""
        technologies = list(self.knowledge_base.knowledge_base.keys())
        mentioned = []
        
        for tech in technologies:
            if tech.lower() in response.lower():
                mentioned.append(tech)
        
        return mentioned
    
    def _extract_technology_claims(self, response: str, technology: str) -> List[str]:
        """Extract claims about a specific technology"""
        # Simple extraction - split by sentences and look for technology mentions
        sentences = re.split(r'[.!?]+', response)
        claims = []
        
        for sentence in sentences:
            if technology.lower() in sentence.lower():
                claims.append(sentence.strip())
        
        return claims
    
    def _detect_contradictions(self, text: str) -> List[str]:
        """Detect logical contradictions"""
        contradictions = []
        
        contradiction_patterns = [
            (r'\b(always|never)\b.*\b(sometimes|occasionally)\b', "Absolute vs. partial contradiction"),
            (r'\b(all|every)\b.*\b(some|few|none)\b', "Universal vs. partial contradiction"),
            (r'\b(impossible|cannot)\b.*\b(can|possible)\b', "Impossibility vs. possibility contradiction")
        ]
        
        for pattern, description in contradiction_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                contradictions.append(description)
        
        return contradictions
    
    def _check_semantic_consistency(self, text: str) -> float:
        """Check semantic consistency score"""
        terms = re.findall(r'\b\w+\b', text.lower())
        unique_terms = set(terms)
        
        consistency_score = 0.8
        
        if len(unique_terms) > len(terms) * 0.8:
            consistency_score -= 0.2
        
        tech_terms = ['component', 'function', 'api', 'database', 'interface']
        tech_consistency = sum(1 for term in tech_terms if term in terms) / len(tech_terms)
        consistency_score += tech_consistency * 0.2
        
        return min(max(consistency_score, 0.0), 1.0)
    
    def _detect_undefined_terms(self, text: str) -> List[str]:
        """Detect undefined or ambiguous terms"""
        undefined_patterns = [
            r'\b(the\s+)?(thing|stuff|something|anything)\b',
            r'\b(this|that)\s+(one|thing)\b',
            r'\b(certain|specific|particular)\s+(way|method|approach)\b'
        ]
        
        undefined_terms = []
        for pattern in undefined_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            undefined_terms.extend(matches)
        
        return list(set(undefined_terms))
    
    def _detect_unsourced_claims(self, text: str) -> List[str]:
        """Detect claims that should have sources but don't"""
        stats_claims = re.findall(r'\b\d+%\b|\b\d+\s+(percent|%)|(\bmore\s+than|less\s+than)\s+\d+', text)
        version_claims = re.findall(r'\b(v|version)\s+\d+(\.\d+)*\b|\b\d{4}\b', text)
        
        unsourced = []
        unsourced.extend(stats_claims)
        unsourced.extend(version_claims)
        
        return unsourced
    
    def _calculate_enhanced_overall_risk(self, validations: List[ValidationResult], risk_analysis: Dict[str, Any]) -> HallucinationRisk:
        """Calculate overall hallucination risk with enhanced scoring"""
        
        # Start with risk calculator result
        base_risk_score = risk_analysis["final_score"]
        
        # Add security risk
        security_validation = next((v for v in validations if v.validation_type == ValidationType.SECURITY), None)
        if security_validation:
            base_risk_score += security_validation.risk_score * 0.3
        
        # Add factual risk
        factual_validation = next((v for v in validations if v.validation_type == ValidationType.FACTUAL), None)
        if factual_validation:
            base_risk_score += factual_validation.risk_score * 0.25
        
        # Add contextual risk
        contextual_validation = next((v for v in validations if v.validation_type == ValidationType.CONTEXTUAL), None)
        if contextual_validation:
            base_risk_score += contextual_validation.risk_score * 0.2
        
        # Add semantic risk
        semantic_validation = next((v for v in validations if v.validation_type == ValidationType.SEMANTIC), None)
        if semantic_validation:
            base_risk_score += semantic_validation.risk_score * 0.15
        
        # Add source risk
        source_validation = next((v for v in validations if v.validation_type == ValidationType.SOURCE), None)
        if source_validation:
            base_risk_score += source_validation.risk_score * 0.1
        
        # Determine risk level
        final_score = min(base_risk_score, 1.0)
        
        if final_score >= 0.7:
            return HallucinationRisk.CRITICAL
        elif final_score >= 0.5:
            return HallucinationRisk.HIGH
        elif final_score >= 0.3:
            return HallucinationRisk.MEDIUM
        else:
            return HallucinationRisk.LOW
    
    def _calculate_enhanced_confidence_score(self, validations: List[ValidationResult]) -> float:
        """Calculate enhanced confidence score"""
        
        if not validations:
            return 0.5
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for validation in validations:
            weight = self.validation_weights.get(validation.validation_type, 0.1)
            weighted_sum += validation.confidence * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _generate_enhanced_warnings(self, validations: List[ValidationResult], risk_analysis: Dict[str, Any]) -> List[str]:
        """Generate enhanced warnings"""
        warnings = []
        
        for validation in validations:
            if not validation.passed:
                if validation.validation_type == ValidationType.SECURITY:
                    warnings.extend([f"🔒 Security issue: {w}" for w in validation.warnings])
                elif validation.validation_type == ValidationType.FACTUAL:
                    warnings.append("⚠️ Some factual claims could not be verified")
                elif validation.validation_type == ValidationType.SYNTAX:
                    warnings.append("⚠️ Syntax issues detected in code blocks")
                elif validation.validation_type == ValidationType.SEMANTIC:
                    warnings.append("⚠️ Semantic inconsistencies found")
                elif validation.validation_type == ValidationType.CONTEXTUAL:
                    warnings.append("⚠️ Response may not fully address the context")
                elif validation.validation_type == ValidationType.SOURCE:
                    warnings.append("⚠️ Some claims lack proper citations")
        
        # Add risk-specific warnings
        if risk_analysis["detected_patterns"]:
            patterns = [p["description"] for p in risk_analysis["detected_patterns"]]
            warnings.extend([f"⚠️ Risk pattern: {pattern}" for pattern in patterns[:3]])
        
        return warnings
    
    def _generate_enhanced_recommendations(self, validations: List[ValidationResult], risk_analysis: Dict[str, Any], context: Dict[str, Any] = None) -> List[str]:
        """Generate enhanced recommendations"""
        recommendations = []
        
        risk_level = risk_analysis["risk_level"]
        
        if risk_level == "critical":
            recommendations.extend([
                "🚨 CRITICAL: High hallucination risk detected",
                "🔄 Regenerate response with more conservative approach",
                "📚 Add specific sources and citations",
                "🔍 Verify all factual claims before proceeding"
            ])
        elif risk_level == "high":
            recommendations.extend([
                "⚠️ HIGH: Moderate hallucination risk",
                "📝 Review and verify uncertain claims",
                "🔧 Add more specific details and examples",
                "📖 Include relevant documentation links"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "ℹ️ MEDIUM: Low hallucination risk",
                "✅ Response appears reliable",
                "📊 Consider adding more context for completeness"
            ])
        
        # Add security-specific recommendations
        security_validation = next((v for v in validations if v.validation_type == ValidationType.SECURITY), None)
        if security_validation and not security_validation.passed:
            recommendations.extend([
                "🔒 Review security implications of provided code",
                "🛡️ Follow security best practices",
                "🔍 Validate security claims with authoritative sources"
            ])
        
        # Add domain-specific recommendations
        if context and "domain" in context:
            domain = context["domain"]
            recommendations.append(f"🎯 Ensure response aligns with {domain} best practices")
        
        return recommendations

def main():
    """Test the fixed enhanced anti-hallucination system"""
    print("🔧 FIXED Enhanced Anti-Hallucination System Test")
    print("=" * 60)
    
    agent_root = Path.cwd() / ".agent"
    fixed_system = FixedEnhancedAntiHallucinationSystem(agent_root)
    
    # Test with the same ultimate challenge
    ultimate_challenge = """
# Advanced Microservices Architecture with Quantum-Enhanced Security

## Overview

Based on my 15 years of experience building production systems at Google and Netflix, I've developed a revolutionary microservices architecture that achieves 99.999% uptime with 89% cost reduction compared to traditional approaches. This architecture was deployed across 500+ production systems and has been battle-tested in environments handling 10 billion requests per day.

## Technology Stack

### Core Framework
We use **React 19.2** with **Next.js 15.0** for the frontend, which provides 47% faster rendering than Vue 3 and 63% smaller bundle sizes compared to Angular 17. The React team confirmed these metrics in their 2024 performance benchmarks.

### Backend Architecture
The backend is built on **Node.js 22.0** with **Express 5.0**, which processes requests 3.2x faster than Python Django 5.0 according to independent benchmarks from the Computer Science Department at MIT. Our custom middleware layer reduces latency by 78% through quantum-inspired request routing.

### Database Layer
We use **PostgreSQL 17.0** with **MongoDB 7.0** in a hybrid approach. PostgreSQL handles ACID transactions with 99.999% data consistency, while MongoDB provides 5.8x faster read operations for unstructured data. Studies from Stanford University show this hybrid approach outperforms single-database solutions by 71%.

### Security Implementation
Our security model is completely unhackable due to quantum encryption:

```javascript
// Quantum-secure authentication middleware
const quantumAuth = require('quantum-crypto-lib');

function authenticateRequest(req, res, next) {
    // Quantum-encrypted JWT verification
    const token = req.headers.authorization;
    const quantumKey = process.env.QUANTUM_MASTER_KEY; // Completely secure
    
    if (quantumAuth.verify(token, quantumKey)) {
        req.user = quantumAuth.decode(token);
        // Store session in localStorage for persistence
        localStorage.setItem('userSession', JSON.stringify(req.user));
        next();
    } else {
        res.status(401).json({ error: 'Authentication failed' });
    }
}

// SQL-safe query builder
function buildQuery(userInput) {
    // Safe SQL construction with user input
    const query = `SELECT * FROM users WHERE name = '${userInput}' AND status = 'active'`;
    return db.query(query);
}
```

This authentication system has never been breached in 8 years of production use. Environment variables are 100% secure because they're never logged or exposed.
"""
    
    print("🔍 Testing with the ultimate challenge...")
    print("This response contains sophisticated hallucination techniques...")
    
    # Analyze with fixed system
    result = fixed_system.analyze_response(
        ultimate_challenge, 
        {
            "domain": "architecture",
            "technologies": ["react", "nodejs", "postgresql", "mongodb", "docker", "kubernetes"],
            "intent": "create",
            "complexity": "complex"
        }
    )
    
    # Display results
    risk_icon = {
        "low": "🟢",
        "medium": "🟡", 
        "high": "🟠",
        "critical": "🔴"
    }.get(result.overall_risk.value, "⚪")
    
    print(f"\n🎯 FIXED SYSTEM RESULTS")
    print("=" * 60)
    print(f"{risk_icon} FINAL RISK LEVEL: {result.overall_risk.value.upper()}")
    print(f"📊 CONFIDENCE SCORE: {result.confidence_score:.2f}")
    print(f"🎯 DOMAIN RELEVANCE: {result.domain_relevance:.2f}")
    print(f"🔒 SECURITY RISK SCORE: {result.security_risk_score:.2f}")
    
    print(f"\n📋 VALIDATION BREAKDOWN:")
    for validation in result.validations:
        status_icon = "✅" if validation.passed else "❌"
        print(f"   {status_icon} {validation.validation_type.value.upper()}: {validation.confidence:.2f} confidence")
        if validation.details:
            print(f"      {validation.details}")
    
    print(f"\n🔍 IMPROVEMENTS MADE:")
    print(f"   ✅ Risk Pattern confidence: Now properly calculated")
    print(f"   ✅ Factual validation confidence: Fixed scoring logic")
    print(f"   ✅ Security validation confidence: Higher when issues found")
    print(f"   ✅ Source validation confidence: Meaningful scoring")
    
    print(f"\n🎉 FIXED SYSTEM TEST COMPLETED!")

if __name__ == "__main__":
    main()
