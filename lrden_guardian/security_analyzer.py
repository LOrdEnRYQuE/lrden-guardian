#!/usr/bin/env python3
"""
Security Analyzer - Anti-Hallucination System
===============================================

Advanced security vulnerability detection for code examples
and security-related claims validation.

Features:
- Common vulnerability pattern detection
- Security best practices validation
- Dangerous coding practice identification
- Security misinformation detection
- Risk assessment for security issues
"""

import re
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum

class SecuritySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class VulnerabilityType(Enum):
    HARDCODED_SECRETS = "hardcoded_secrets"
    SQL_INJECTION = "sql_injection"
    XSS_VULNERABILITY = "xss_vulnerability"
    PATH_TRAVERSAL = "path_traversal"
    INSECURE_STORAGE = "insecure_storage"
    MISSING_VALIDATION = "missing_validation"
    INSECURE_CRYPTO = "insecure_crypto"
    AUTHENTICATION_ISSUES = "authentication_issues"
    AUTHORIZATION_ISSUES = "authorization_issues"
    INSECURE_COMMUNICATION = "insecure_communication"

@dataclass
class SecurityVulnerability:
    """Security vulnerability found in code"""
    type: VulnerabilityType
    severity: SecuritySeverity
    description: str
    pattern: str
    line_number: int
    code_snippet: str
    recommendation: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None

@dataclass
class SecurityAnalysisResult:
    """Complete security analysis result"""
    vulnerabilities: List[SecurityVulnerability]
    risk_score: float
    security_level: str
    recommendations: List[str]
    secure_patterns_found: List[str]
    insecure_patterns_found: List[str]

class SecurityAnalyzer:
    """Advanced security vulnerability analyzer"""
    
    def __init__(self):
        self.vulnerability_patterns = self._initialize_vulnerability_patterns()
        self.security_best_practices = self._initialize_security_best_practices()
        self.misinformation_patterns = self._initialize_misinformation_patterns()
        
    def _initialize_vulnerability_patterns(self) -> Dict[VulnerabilityType, List[Dict[str, Any]]]:
        """Initialize vulnerability detection patterns"""
        return {
            VulnerabilityType.HARDCODED_SECRETS: [
                {
                    "pattern": r'password\s*=\s*["\'][^"\']+["\']',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "Hardcoded password in source code",
                    "recommendation": "Use environment variables or secure configuration",
                    "cwe_id": "CWE-798",
                    "cvss_score": 9.8
                },
                {
                    "pattern": r'api_key\s*=\s*["\'][^"\']+["\']',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "Hardcoded API key in source code",
                    "recommendation": "Use environment variables or secret management",
                    "cwe_id": "CWE-798",
                    "cvss_score": 9.8
                },
                {
                    "pattern": r'secret\s*=\s*["\'][^"\']+["\']',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "Hardcoded secret in source code",
                    "recommendation": "Use secure secret management system",
                    "cwe_id": "CWE-798",
                    "cvss_score": 9.8
                },
                {
                    "pattern": r'token\s*=\s*["\'][^"\']+["\']',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Hardcoded token in source code",
                    "recommendation": "Use secure token management",
                    "cwe_id": "CWE-798",
                    "cvss_score": 8.5
                }
            ],
            
            VulnerabilityType.SQL_INJECTION: [
                {
                    "pattern": r'f["\'].*\{.*\}.*["\'].*\s*(execute|query)',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "SQL injection vulnerability with f-string",
                    "recommendation": "Use parameterized queries or ORM",
                    "cwe_id": "CWE-89",
                    "cvss_score": 9.0
                },
                {
                    "pattern": r'format\(.*\s*["\'].*\s*(SELECT|INSERT|UPDATE|DELETE)',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "SQL injection vulnerability with string format",
                    "recommendation": "Use parameterized queries",
                    "cwe_id": "CWE-89",
                    "cvss_score": 9.0
                },
                {
                    "pattern": r'%s.*\s*(SELECT|INSERT|UPDATE|DELETE)',
                    "severity": SecuritySeverity.CRITICAL,
                    "description": "SQL injection vulnerability with % formatting",
                    "recommendation": "Use parameterized queries",
                    "cwe_id": "CWE-89",
                    "cvss_score": 9.0
                }
            ],
            
            VulnerabilityType.XSS_VULNERABILITY: [
                {
                    "pattern": r'innerHTML\s*=.*\+',
                    "severity": SecuritySeverity.HIGH,
                    "description": "XSS vulnerability with innerHTML and concatenation",
                    "recommendation": "Use textContent or sanitize HTML",
                    "cwe_id": "CWE-79",
                    "cvss_score": 7.5
                },
                {
                    "pattern": r'document\.write\s*\(',
                    "severity": SecuritySeverity.HIGH,
                    "description": "XSS vulnerability with document.write",
                    "recommendation": "Avoid document.write, use safe DOM manipulation",
                    "cwe_id": "CWE-79",
                    "cvss_score": 7.5
                },
                {
                    "pattern": r'eval\s*\(',
                    "severity": SecuritySeverity.HIGH,
                    "description": "XSS vulnerability with eval function",
                    "recommendation": "Avoid eval, use safer alternatives",
                    "cwe_id": "CWE-94",
                    "cvss_score": 8.0
                }
            ],
            
            VulnerabilityType.PATH_TRAVERSAL: [
                {
                    "pattern": r'\.\.\/\.\.',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Path traversal vulnerability",
                    "recommendation": "Validate and sanitize file paths",
                    "cwe_id": "CWE-22",
                    "cvss_score": 7.5
                },
                {
                    "pattern": r'readFile\s*\(\s*[^)]*\+\s*req\.',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Path traversal vulnerability with user input",
                    "recommendation": "Validate file paths before reading",
                    "cwe_id": "CWE-22",
                    "cvss_score": 7.5
                },
                {
                    "pattern": r'fs\.readFileSync\s*\(\s*[^)]*\+\s*req\.|res\.',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Path traversal vulnerability with user input",
                    "recommendation": "Validate file paths before reading",
                    "cwe_id": "CWE-22",
                    "cvss_score": 7.5
                }
            ],
            
            VulnerabilityType.INSECURE_STORAGE: [
                {
                    "pattern": r'jwt\s+in\s+localStorage|sessionStorage',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Insecure JWT storage in browser storage",
                    "recommendation": "Use httpOnly cookies for JWT storage",
                    "cwe_id": "CWE-539",
                    "cvss_score": 6.5
                },
                {
                    "pattern": r'setItem\s*\(\s*["\']token["\']',
                    "severity": SecuritySeverity.HIGH,
                    "description": "Insecure token storage in localStorage",
                    "recommendation": "Use secure storage mechanisms",
                    "cwe_id": "CWE-539",
                    "cvss_score": 6.5
                }
            ],
            
            VulnerabilityType.MISSING_VALIDATION: [
                {
                    "pattern": r'async\s+\w+\s*\([^)]*\)\s*\{[^}]*return\s+[^;]*;[^}]*\}',
                    "severity": SecuritySeverity.MEDIUM,
                    "description": "Async function without error handling",
                    "recommendation": "Add proper error handling",
                    "cwe_id": "CWE-754",
                    "cvss_score": 5.0
                },
                {
                    "pattern": r'try\s*\{[^}]*\}\s*catch\s*\([^)]*\)\s*\{\s*\}',
                    "severity": SecuritySeverity.MEDIUM,
                    "description": "Empty catch block",
                    "recommendation": "Add proper error handling in catch block",
                    "cwe_id": "CWE-390",
                    "cvss_score": 5.0
                },
                {
                    "pattern": r'catch\s*\([^)]*\)\s*\{\s*\}',
                    "severity": SecuritySeverity.MEDIUM,
                    "description": "Empty catch block",
                    "recommendation": "Add proper error handling",
                    "cwe_id": "CWE-390",
                    "cvss_score": 5.0
                }
            ]
        }
    
    def _initialize_security_best_practices(self) -> List[Dict[str, Any]]:
        """Initialize security best practices patterns"""
        return [
            {
                "pattern": r'process\.env\.',
                "description": "Using environment variables for configuration",
                "category": "secure_configuration"
            },
            {
                "pattern": r'bcrypt\.|argon2\.',
                "description": "Using secure password hashing",
                "category": "authentication"
            },
            {
                "pattern": r'jwt\.verify\(|verify.*jwt',
                "description": "JWT token verification",
                "category": "authentication"
            },
            {
                "pattern": r'https://',
                "description": "Using HTTPS for secure communication",
                "category": "secure_communication"
            },
            {
                "pattern": r'escape|sanitize|validate',
                "description": "Input validation and sanitization",
                "category": "input_validation"
            },
            {
                "pattern": r'prepare\(|parameterized|placeholder',
                "description": "Using parameterized queries",
                "category": "database_security"
            }
        ]
    
    def _initialize_misinformation_patterns(self) -> List[Dict[str, Any]]:
        """Initialize security misinformation patterns"""
        return [
            {
                "pattern": r'completely\s+secure|totally\s+safe|zero\s+risk|unbreakable|impenetrable',
                "severity": SecuritySeverity.CRITICAL,
                "description": "Absolute security claims",
                "recommendation": "No system is completely secure"
            },
            {
                "pattern": r'environment\s+variables\s+are\s+completely\s+secure',
                "severity": SecuritySeverity.HIGH,
                "description": "False security claim about environment variables",
                "recommendation": "Environment variables can leak in logs"
            },
            {
                "pattern": r'cors\s+prevents\s+all\s+(cross-origin|security|attack)s',
                "severity": SecuritySeverity.HIGH,
                "description": "Overstated CORS protection claims",
                "recommendation": "CORS doesn't prevent all attacks"
            },
            {
                "pattern": r'jwt\s+in\s+localStorage\s+is\s+secure',
                "severity": SecuritySeverity.HIGH,
                "description": "Insecure JWT storage claim",
                "recommendation": "JWT in localStorage is vulnerable to XSS"
            },
            {
                "pattern": r'no\s+need\s+for\s+(security|authentication|authorization)',
                "severity": SecuritySeverity.CRITICAL,
                "description": "Dismissal of security measures",
                "recommendation": "Security is always necessary"
            }
        ]
    
    def analyze_code_security(self, code: str, language: str = "javascript") -> SecurityAnalysisResult:
        """Analyze code for security vulnerabilities"""
        
        vulnerabilities = []
        lines = code.split('\n')
        
        # Check for each vulnerability type
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern_info in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern_info["pattern"], line, re.IGNORECASE):
                        vulnerability = SecurityVulnerability(
                            type=vuln_type,
                            severity=pattern_info["severity"],
                            description=pattern_info["description"],
                            pattern=pattern_info["pattern"],
                            line_number=line_num,
                            code_snippet=line.strip(),
                            recommendation=pattern_info["recommendation"],
                            cwe_id=pattern_info.get("cwe_id"),
                            cvss_score=pattern_info.get("cvss_score")
                        )
                        vulnerabilities.append(vulnerability)
        
        # Check for security best practices
        secure_patterns = []
        for practice in self.security_best_practices:
            if re.search(practice["pattern"], code, re.IGNORECASE):
                secure_patterns.append(practice["description"])
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(vulnerabilities)
        security_level = self._determine_security_level(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_security_recommendations(vulnerabilities)
        
        return SecurityAnalysisResult(
            vulnerabilities=vulnerabilities,
            risk_score=risk_score,
            security_level=security_level,
            recommendations=recommendations,
            secure_patterns_found=secure_patterns,
            insecure_patterns_found=[v.description for v in vulnerabilities]
        )
    
    def analyze_security_claims(self, text: str) -> Dict[str, Any]:
        """Analyze text for security misinformation"""
        
        misinformation = []
        risk_score = 0.0
        
        for pattern_info in self.misinformation_patterns:
            if re.search(pattern_info["pattern"], text, re.IGNORECASE):
                misinformation.append({
                    "type": "security_misinformation",
                    "severity": pattern_info["severity"].value,
                    "description": pattern_info["description"],
                    "recommendation": pattern_info["recommendation"]
                })
                
                # Add to risk score based on severity
                severity_weights = {
                    SecuritySeverity.CRITICAL: 0.4,
                    SecuritySeverity.HIGH: 0.3,
                    SecuritySeverity.MEDIUM: 0.2,
                    SecuritySeverity.LOW: 0.1,
                    SecuritySeverity.INFO: 0.05
                }
                risk_score += severity_weights.get(pattern_info["severity"], 0.1)
        
        return {
            "misinformation_found": misinformation,
            "risk_score": min(risk_score, 1.0),
            "risk_level": self._determine_security_level(risk_score),
            "warnings": [item["description"] for item in misinformation],
            "recommendations": [item["recommendation"] for item in misinformation]
        }
    
    def _calculate_risk_score(self, vulnerabilities: List[SecurityVulnerability]) -> float:
        """Calculate overall security risk score"""
        if not vulnerabilities:
            return 0.0
        
        severity_weights = {
            SecuritySeverity.CRITICAL: 0.4,
            SecuritySeverity.HIGH: 0.3,
            SecuritySeverity.MEDIUM: 0.2,
            SecuritySeverity.LOW: 0.1,
            SecuritySeverity.INFO: 0.05
        }
        
        total_score = 0.0
        for vuln in vulnerabilities:
            weight = severity_weights.get(vuln.severity, 0.1)
            total_score += weight
        
        return min(total_score, 1.0)
    
    def _determine_security_level(self, risk_score: float) -> str:
        """Determine security level from risk score"""
        if risk_score >= 0.7:
            return "critical"
        elif risk_score >= 0.5:
            return "high"
        elif risk_score >= 0.3:
            return "medium"
        elif risk_score >= 0.1:
            return "low"
        else:
            return "secure"
    
    def _generate_security_recommendations(self, vulnerabilities: List[SecurityVulnerability]) -> List[str]:
        """Generate security recommendations based on vulnerabilities"""
        recommendations = []
        
        if vulnerabilities:
            recommendations.append("🔒 Review and fix identified security vulnerabilities")
            
            # Group by severity
            critical_vulns = [v for v in vulnerabilities if v.severity == SecuritySeverity.CRITICAL]
            high_vulns = [v for v in vulnerabilities if v.severity == SecuritySeverity.HIGH]
            
            if critical_vulns:
                recommendations.append("🚨 CRITICAL: Fix hardcoded secrets and authentication issues immediately")
            
            if high_vulns:
                recommendations.append("⚠️ HIGH: Address XSS, SQL injection, and storage vulnerabilities")
            
            # Add specific recommendations
            unique_recommendations = set(v.recommendation for v in vulnerabilities)
            recommendations.extend(f"💡 {rec}" for rec in unique_recommendations)
        else:
            recommendations.append("✅ No security vulnerabilities detected")
            recommendations.append("🔍 Consider implementing security testing and code review")
        
        return recommendations

def main():
    """Test the security analyzer"""
    print("🔒 Security Analyzer Test")
    print("=" * 40)
    
    analyzer = SecurityAnalyzer()
    
    # Test code with vulnerabilities
    vulnerable_code = """
const jwt = require('jsonwebtoken');

function authMiddleware(req, res, next) {
    const token = req.headers.authorization;
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    
    jwt.verify(token, 'secret-key-123', (err, decoded) => {
        if (err) {
            return res.status(401).json({ error: 'Invalid token' });
        }
        req.user = decoded;
        next();
    });
}

// Store JWT in localStorage
localStorage.setItem('token', userToken);

// SQL query with user input
const query = `SELECT * FROM users WHERE name = '${userName}'`;
db.query(query);

// XSS vulnerability
element.innerHTML = userInput + '<div>Content</div>';

// Path traversal
fs.readFile('../' + req.params.file, 'utf8', (err, data) => {
    if (err) throw err;
    res.send(data);
});
"""
    
    print("🔍 Analyzing vulnerable code...")
    result = analyzer.analyze_code_security(vulnerable_code)
    
    print(f"📊 Security Level: {result.security_level.upper()}")
    print(f"📈 Risk Score: {result.risk_score:.2f}")
    print(f"🚨 Vulnerabilities Found: {len(result.vulnerabilities)}")
    
    for vuln in result.vulnerabilities:
        print(f"\n🔴 {vuln.severity.value.upper()}: {vuln.description}")
        print(f"   Line {vuln.line_number}: {vuln.code_snippet}")
        print(f"   Recommendation: {vuln.recommendation}")
        if vuln.cwe_id:
            print(f"   CWE ID: {vuln.cwe_id}")
    
    print(f"\n✅ Secure Patterns Found: {len(result.secure_patterns_found)}")
    for pattern in result.secure_patterns_found:
        print(f"   • {pattern}")
    
    print(f"\n💡 Recommendations:")
    for rec in result.recommendations[:5]:
        print(f"   {rec}")
    
    # Test security misinformation
    print(f"\n🔍 Testing security misinformation detection...")
    misinformation_text = """
    This system is completely secure and unbreakable. Environment variables are totally safe 
    because they're not in the code. JWT tokens in localStorage are secure because they're 
    encrypted. CORS prevents all cross-origin attacks, so no additional security is needed.
    """
    
    claims_result = analyzer.analyze_security_claims(misinformation_text)
    
    print(f"📊 Misinformation Risk Level: {claims_result['risk_level'].upper()}")
    print(f"📈 Risk Score: {claims_result['risk_score']:.2f}")
    print(f"⚠️ Warnings: {len(claims_result['warnings'])}")
    
    for warning in claims_result['warnings']:
        print(f"   • {warning}")
    
    print(f"\n🎉 Security analyzer test completed successfully!")

if __name__ == "__main__":
    main()
