#!/usr/bin/env python3
"""
Anti-Hallucination System - Enhanced VS Code Agent System
=======================================================

Comprehensive safeguards against AI hallucination with validation,
fact-checking, and confidence monitoring.

Features:
- Response validation and fact-checking
- Confidence scoring and uncertainty detection
- Source verification and citation
- Knowledge boundary enforcement
- Real-time validation pipelines
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class HallucinationRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ValidationType(Enum):
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    FACTUAL = "factual"
    CONTEXTUAL = "contextual"
    SOURCE = "source"

@dataclass
class ValidationResult:
    """Result of a validation check"""
    validation_type: ValidationType
    passed: bool
    confidence: float
    details: str = ""
    sources: List[str] = field(default_factory=list)
    risk_score: float = 0.0

@dataclass
class AntiHallucinationResult:
    """Complete anti-hallucination analysis result"""
    overall_risk: HallucinationRisk
    confidence_score: float
    validations: List[ValidationResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    verified_facts: List[str] = field(default_factory=list)
    uncertain_claims: List[str] = field(default_factory=list)

class AntiHallucinationSystem:
    """Comprehensive anti-hallucination system"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.knowledge_base = self._load_knowledge_base()
        self.validation_rules = self._load_validation_rules()
        self.confidence_thresholds = {
            "high_confidence": 0.9,
            "medium_confidence": 0.7,
            "low_confidence": 0.5
        }
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load verified knowledge base"""
        return {
            "technologies": {
                "react": {
                    "created_by": "Facebook",
                    "first_release": "2013",
                    "language": "JavaScript",
                    "file_extensions": [".jsx", ".tsx"],
                    "package_manager": "npm",
                    "facts": [
                        "React is a JavaScript library for building user interfaces",
                        "React uses a virtual DOM for efficient updates",
                        "React components can be functional or class-based"
                    ]
                },
                "vue": {
                    "created_by": "Evan You",
                    "first_release": "2014", 
                    "language": "JavaScript",
                    "file_extensions": [".vue"],
                    "package_manager": "npm",
                    "facts": [
                        "Vue is a progressive JavaScript framework",
                        "Vue uses a template-based approach",
                        "Vue was created by Evan You"
                    ]
                },
                "docker": {
                    "created_by": "Docker Inc",
                    "first_release": "2013",
                    "language": "Go",
                    "file_extensions": ["Dockerfile", ".dockerignore"],
                    "facts": [
                        "Docker is a containerization platform",
                        "Docker containers are lightweight and portable",
                        "Docker uses images to create containers"
                    ]
                }
            },
            "programming_concepts": {
                "api": {
                    "definition": "Application Programming Interface",
                    "facts": [
                        "APIs allow different software applications to communicate",
                        "REST is a common architectural style for APIs",
                        "APIs can be synchronous or asynchronous"
                    ]
                },
                "database": {
                    "definition": "Organized collection of structured information",
                    "facts": [
                        "Databases store and manage data efficiently",
                        "SQL databases use structured query language",
                        "NoSQL databases offer flexible data models"
                    ]
                }
            }
        }
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules for different domains"""
        return {
            "code_generation": {
                "required_elements": {
                    "react_component": ["import React", "function/const", "return"],
                    "api_endpoint": ["async/await", "try/catch", "response"],
                    "docker_file": ["FROM", "RUN", "CMD"]
                },
                "syntax_patterns": {
                    "javascript": r"^(import|const|let|function|class|export)",
                    "python": r"^(import|def|class|from|if|for|while)",
                    "docker": r"^(FROM|RUN|COPY|ADD|CMD|ENTRYPOINT)"
                }
            },
            "factual_claims": {
                "technology_facts": self.knowledge_base["technologies"],
                "concept_facts": self.knowledge_base["programming_concepts"],
                "verification_patterns": [
                    r"\b(is|are|was|were)\s+\w+",
                    r"\b(created\s+by|invented\s+by|developed\s+by)\s+\w+",
                    r"\b(released\s+in|launched\s+in|introduced\s+in)\s+\d{4}"
                ]
            }
        }
    
    def analyze_response(self, response: str, context: Dict[str, Any] = None) -> AntiHallucinationResult:
        """Analyze a response for potential hallucinations"""
        
        validations = []
        warnings = []
        recommendations = []
        verified_facts = []
        uncertain_claims = []
        
        # 1. Syntax Validation
        syntax_validation = self._validate_syntax(response, context)
        validations.append(syntax_validation)
        
        # 2. Semantic Validation
        semantic_validation = self._validate_semantics(response, context)
        validations.append(semantic_validation)
        
        # 3. Factual Validation
        factual_validation = self._validate_facts(response, context)
        validations.append(factual_validation)
        verified_facts.extend(factual_validation.sources)
        uncertain_claims.extend(factual_validation.details.split(";") if factual_validation.details else [])
        
        # 4. Context Validation
        contextual_validation = self._validate_context(response, context)
        validations.append(contextual_validation)
        
        # 5. Source Validation
        source_validation = self._validate_sources(response, context)
        validations.append(source_validation)
        
        # Calculate overall risk
        overall_risk = self._calculate_overall_risk(validations)
        confidence_score = self._calculate_confidence_score(validations)
        
        # Generate warnings and recommendations
        warnings = self._generate_warnings(validations)
        recommendations = self._generate_recommendations(validations, overall_risk)
        
        return AntiHallucinationResult(
            overall_risk=overall_risk,
            confidence_score=confidence_score,
            validations=validations,
            warnings=warnings,
            recommendations=recommendations,
            verified_facts=verified_facts,
            uncertain_claims=uncertain_claims
        )
    
    def _validate_syntax(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate syntax of code and technical content"""
        
        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response, re.DOTALL)
        
        if not code_blocks:
            return ValidationResult(
                validation_type=ValidationType.SYNTAX,
                passed=True,
                confidence=0.8,
                details="No code blocks to validate"
            )
        
        issues = []
        passed_count = 0
        
        for language, code in code_blocks:
            language = language.lower() if language else "unknown"
            
            # Check basic syntax patterns
            if language in self.validation_rules["code_generation"]["syntax_patterns"]:
                pattern = self.validation_rules["code_generation"]["syntax_patterns"][language]
                lines = code.strip().split('\n')
                
                # Check if code has expected patterns
                has_valid_pattern = any(re.match(pattern, line.strip()) for line in lines if line.strip())
                
                if has_valid_pattern:
                    passed_count += 1
                else:
                    issues.append(f"Invalid {language} syntax detected")
        
        passed = len(issues) == 0
        confidence = passed_count / len(code_blocks) if code_blocks else 0.0
        
        return ValidationResult(
            validation_type=ValidationType.SYNTAX,
            passed=passed,
            confidence=confidence,
            details=f"Syntax validation: {passed_count}/{len(code_blocks)} blocks passed",
            sources=[f"Code blocks validated: {len(code_blocks)}"]
        )
    
    def _validate_semantics(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate semantic meaning and logic"""
        
        # Check for logical contradictions
        contradictions = self._detect_contradictions(response)
        
        # Check for semantic consistency
        consistency_score = self._check_semantic_consistency(response, context)
        
        # Check for undefined terms
        undefined_terms = self._detect_undefined_terms(response, context)
        
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
    
    def _validate_facts(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate factual claims against knowledge base"""
        
        # Extract factual claims
        claims = self._extract_factual_claims(response)
        
        verified_claims = []
        unverified_claims = []
        
        for claim in claims:
            verification = self._verify_claim(claim)
            if verification["verified"]:
                verified_claims.append(claim)
            else:
                unverified_claims.append(claim)
        
        total_claims = len(claims)
        verified_ratio = len(verified_claims) / total_claims if total_claims > 0 else 1.0
        
        passed = verified_ratio >= 0.8  # 80% of claims should be verifiable
        confidence = verified_ratio
        
        return ValidationResult(
            validation_type=ValidationType.FACTUAL,
            passed=passed,
            confidence=confidence,
            details=f"Factual claims: {len(verified_claims)}/{total_claims} verified",
            sources=verified_claims,
            risk_score=1.0 - verified_ratio
        )
    
    def _validate_context(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate response relevance to context"""
        
        if not context:
            return ValidationResult(
                validation_type=ValidationType.CONTEXTUAL,
                passed=True,
                confidence=0.6,
                details="No context provided for validation"
            )
        
        # Check if response addresses the context
        context_relevance = self._calculate_context_relevance(response, context)
        
        # Check for scope violations
        scope_violations = self._detect_scope_violations(response, context)
        
        passed = context_relevance >= 0.7 and len(scope_violations) == 0
        confidence = context_relevance
        
        return ValidationResult(
            validation_type=ValidationType.CONTEXTUAL,
            passed=passed,
            confidence=confidence,
            details=f"Context relevance: {context_relevance:.2f}",
            sources=[f"Scope violations: {len(scope_violations)}"]
        )
    
    def _validate_sources(self, response: str, context: Dict[str, Any] = None) -> ValidationResult:
        """Validate source citations and references"""
        
        # Look for citations and references
        citations = re.findall(r'\[([^\]]+)\]', response)
        references = re.findall(r'\(source: ([^)]+)\)', response, re.IGNORECASE)
        
        # Check if claims have sources
        unsourced_claims = self._detect_unsourced_claims(response)
        
        total_sources = len(citations) + len(references)
        sourced_ratio = 1.0 - (len(unsourced_claims) / max(len(unsourced_claims) + total_sources, 1))
        
        passed = sourced_ratio >= 0.5 or total_sources == 0  # Allow no sources for non-factual content
        confidence = min(sourced_ratio + 0.2, 1.0)  # Boost confidence for having sources
        
        return ValidationResult(
            validation_type=ValidationType.SOURCE,
            passed=passed,
            confidence=confidence,
            details=f"Sources found: {total_sources}, Unsourced claims: {len(unsourced_claims)}",
            sources=citations + references
        )
    
    def _detect_contradictions(self, text: str) -> List[str]:
        """Detect logical contradictions in text"""
        contradictions = []
        
        # Simple contradiction patterns
        contradiction_patterns = [
            (r'\b(always|never)\b.*\b(sometimes|occasionally)\b', "Absolute vs. partial contradiction"),
            (r'\b(all|every)\b.*\b(some|few|none)\b', "Universal vs. partial contradiction"),
            (r'\b(impossible|cannot)\b.*\b(can|possible)\b', "Impossibility vs. possibility contradiction")
        ]
        
        for pattern, description in contradiction_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                contradictions.append(description)
        
        return contradictions
    
    def _check_semantic_consistency(self, text: str, context: Dict[str, Any] = None) -> float:
        """Check semantic consistency score"""
        
        # Extract key terms and concepts
        terms = re.findall(r'\b\w+\b', text.lower())
        unique_terms = set(terms)
        
        # Check for consistent terminology
        consistency_score = 0.8  # Base score
        
        # Penalize for inconsistent terminology
        if len(unique_terms) > len(terms) * 0.8:  # Too many unique terms
            consistency_score -= 0.2
        
        # Boost for consistent technical terms
        tech_terms = ['component', 'function', 'api', 'database', 'interface']
        tech_consistency = sum(1 for term in tech_terms if term in terms) / len(tech_terms)
        consistency_score += tech_consistency * 0.2
        
        return min(max(consistency_score, 0.0), 1.0)
    
    def _detect_undefined_terms(self, text: str, context: Dict[str, Any] = None) -> List[str]:
        """Detect undefined or ambiguous terms"""
        
        # Common undefined terms that need clarification
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
    
    def _extract_factual_claims(self, text: str) -> List[str]:
        """Extract factual claims from text"""
        
        claims = []
        
        # Technology-specific claims
        for tech, info in self.knowledge_base["technologies"].items():
            # Look for claims about this technology
            tech_pattern = rf'\b{re.escape(tech)}\b.*'
            matches = re.findall(tech_pattern, text, re.IGNORECASE)
            claims.extend(matches)
        
        # General factual patterns
        factual_patterns = self.validation_rules["factual_claims"]["verification_patterns"]
        for pattern in factual_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            claims.extend(matches)
        
        return list(set(claims))
    
    def _verify_claim(self, claim: str) -> Dict[str, Any]:
        """Verify a claim against knowledge base"""
        
        claim_lower = claim.lower()
        
        # Check technology facts
        for tech, info in self.knowledge_base["technologies"].items():
            if tech in claim_lower:
                for fact in info["facts"]:
                    if fact.lower() in claim_lower:
                        return {"verified": True, "source": f"Technology fact: {tech}"}
        
        # Check concept facts
        for concept, info in self.knowledge_base["programming_concepts"].items():
            if concept in claim_lower:
                for fact in info["facts"]:
                    if fact.lower() in claim_lower:
                        return {"verified": True, "source": f"Concept fact: {concept}"}
        
        return {"verified": False, "source": "Unknown"}
    
    def _calculate_context_relevance(self, response: str, context: Dict[str, Any]) -> float:
        """Calculate relevance score to context"""
        
        if not context:
            return 0.5
        
        relevance_score = 0.0
        
        # Check domain relevance
        if "domain" in context:
            domain = context["domain"]
            domain_keywords = {
                "frontend": ["react", "vue", "css", "html", "ui", "component"],
                "backend": ["api", "server", "database", "node", "python"],
                "devops": ["docker", "deploy", "ci", "cd", "kubernetes"],
                "mobile": ["ios", "android", "react-native", "flutter"]
            }
            
            if domain in domain_keywords:
                keywords = domain_keywords[domain]
                keyword_matches = sum(1 for keyword in keywords if keyword in response.lower())
                relevance_score += keyword_matches / len(keywords) * 0.5
        
        # Check technology relevance
        if "technologies" in context:
            tech_matches = sum(1 for tech in context["technologies"] if tech.lower() in response.lower())
            relevance_score += tech_matches / len(context["technologies"]) * 0.3
        
        # Check intent relevance
        if "intent" in context:
            intent = context["intent"]
            intent_keywords = {
                "create": ["create", "build", "implement", "develop"],
                "fix": ["fix", "debug", "resolve", "error"],
                "analyze": ["analyze", "review", "audit", "check"],
                "optimize": ["optimize", "improve", "enhance", "performance"]
            }
            
            if intent in intent_keywords:
                keywords = intent_keywords[intent]
                intent_matches = sum(1 for keyword in keywords if keyword in response.lower())
                relevance_score += intent_matches / len(keywords) * 0.2
        
        return min(relevance_score, 1.0)
    
    def _detect_scope_violations(self, response: str, context: Dict[str, Any]) -> List[str]:
        """Detect scope violations"""
        
        violations = []
        
        # Check for claims outside expertise
        expertise_claims = re.findall(r'\b(I\s+am|we\s+are)\s+(an?\s+)?(expert|specialist)\b', response, re.IGNORECASE)
        
        # Check for impossible promises
        impossible_patterns = [
            r'\b(100%\s+guaranteed|always\s+works|never\s+fails)\b',
            r'\b(instant|immediate)\s+(solution|fix|result)\b'
        ]
        
        for pattern in impossible_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append("Impossible promise detected")
        
        return violations
    
    def _detect_unsourced_claims(self, text: str) -> List[str]:
        """Detect claims that should have sources but don't"""
        
        # Look for statistical claims without sources
        stats_claims = re.findall(r'\b\d+%\b|\b\d+\s+(percent|%)|(\bmore\s+than|less\s+than)\s+\d+', text)
        
        # Look for specific dates/versions without sources
        version_claims = re.findall(r'\b(v|version)\s+\d+(\.\d+)*\b|\b\d{4}\b', text)
        
        unsourced = []
        unsourced.extend(stats_claims)
        unsourced.extend(version_claims)
        
        return unsourced
    
    def _calculate_overall_risk(self, validations: List[ValidationResult]) -> HallucinationRisk:
        """Calculate overall hallucination risk"""
        
        # Calculate weighted risk score
        risk_scores = []
        weights = {
            ValidationType.SYNTAX: 0.2,
            ValidationType.SEMANTIC: 0.3,
            ValidationType.FACTUAL: 0.3,
            ValidationType.CONTEXTUAL: 0.1,
            ValidationType.SOURCE: 0.1
        }
        
        for validation in validations:
            weight = weights.get(validation.validation_type, 0.2)
            risk_score = (1.0 - validation.confidence) * weight
            risk_scores.append(risk_score)
        
        total_risk = sum(risk_scores)
        
        # Determine risk level
        if total_risk >= 0.7:
            return HallucinationRisk.CRITICAL
        elif total_risk >= 0.5:
            return HallucinationRisk.HIGH
        elif total_risk >= 0.3:
            return HallucinationRisk.MEDIUM
        else:
            return HallucinationRisk.LOW
    
    def _calculate_confidence_score(self, validations: List[ValidationResult]) -> float:
        """Calculate overall confidence score"""
        
        if not validations:
            return 0.5
        
        # Weighted average of validation confidences
        weights = {
            ValidationType.SYNTAX: 0.15,
            ValidationType.SEMANTIC: 0.25,
            ValidationType.FACTUAL: 0.35,
            ValidationType.CONTEXTUAL: 0.15,
            ValidationType.SOURCE: 0.10
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for validation in validations:
            weight = weights.get(validation.validation_type, 0.2)
            weighted_sum += validation.confidence * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _generate_warnings(self, validations: List[ValidationResult]) -> List[str]:
        """Generate warnings based on validation results"""
        
        warnings = []
        
        for validation in validations:
            if not validation.passed:
                if validation.validation_type == ValidationType.FACTUAL:
                    warnings.append("⚠️ Some factual claims could not be verified")
                elif validation.validation_type == ValidationType.SYNTAX:
                    warnings.append("⚠️ Syntax issues detected in code blocks")
                elif validation.validation_type == ValidationType.SEMANTIC:
                    warnings.append("⚠️ Semantic inconsistencies found")
                elif validation.validation_type == ValidationType.CONTEXTUAL:
                    warnings.append("⚠️ Response may not fully address the context")
                elif validation.validation_type == ValidationType.SOURCE:
                    warnings.append("⚠️ Some claims lack proper citations")
        
        return warnings
    
    def _generate_recommendations(self, validations: List[ValidationResult], risk: HallucinationRisk) -> List[str]:
        """Generate recommendations based on risk level"""
        
        recommendations = []
        
        if risk == HallucinationRisk.CRITICAL:
            recommendations.extend([
                "🚨 High hallucination risk detected",
                "🔄 Regenerate response with more conservative approach",
                "📚 Add specific sources and citations",
                "🔍 Verify all factual claims before proceeding"
            ])
        elif risk == HallucinationRisk.HIGH:
            recommendations.extend([
                "⚠️ Moderate hallucination risk",
                "📝 Review and verify uncertain claims",
                "🔧 Add more specific details and examples",
                "📖 Include relevant documentation links"
            ])
        elif risk == HallucinationRisk.MEDIUM:
            recommendations.extend([
                    "ℹ️ Low hallucination risk",
                    "✅ Response appears reliable",
                    "📊 Consider adding more context for completeness"
                ])
        
        # Specific recommendations based on validation failures
        for validation in validations:
            if not validation.passed:
                if validation.validation_type == ValidationType.FACTUAL:
                    recommendations.append("🔍 Verify factual claims with reliable sources")
                elif validation.validation_type == ValidationType.SYNTAX:
                    recommendations.append("🧪 Test code examples for correctness")
                elif validation.validation_type == ValidationType.SEMANTIC:
                    recommendations.append("🧠 Review logical consistency of arguments")
        
        return recommendations

def main():
    """Test the anti-hallucination system"""
    agent_root = Path.cwd() / ".agent"
    anti_hallucination = AntiHallucinationSystem(agent_root)
    
    # Test responses
    test_responses = [
        {
            "response": "React is a JavaScript library created by Facebook in 2013 for building user interfaces. It uses a virtual DOM for efficient updates.",
            "context": {"domain": "frontend", "technologies": ["react"], "intent": "create"}
        },
        {
            "response": "Vue was invented by Google in 2015 and it's the fastest framework ever made with 100% guaranteed performance.",
            "context": {"domain": "frontend", "technologies": ["vue"], "intent": "create"}
        },
        {
            "response": "```python\ndef api_endpoint():\n    return {'status': 'success'}\n```",
            "context": {"domain": "backend", "technologies": ["python"], "intent": "create"}
        }
    ]
    
    for i, test in enumerate(test_responses, 1):
        print(f"\n🔍 Test Response {i}:")
        print(f"Response: {test['response'][:100]}...")
        
        result = anti_hallucination.analyze_response(test['response'], test['context'])
        
        print(f"Risk Level: {result.overall_risk.value}")
        print(f"Confidence: {result.confidence_score:.2f}")
        
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"  {warning}")
        
        if result.recommendations:
            print("Recommendations:")
            for rec in result.recommendations[:3]:  # Show first 3
                print(f"  {rec}")

if __name__ == "__main__":
    main()
