#!/usr/bin/env python3
"""
Simple test for enhanced knowledge base functionality
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime, timezone

@dataclass
class TechnologyFact:
    """Verified fact about a technology"""
    fact: str
    source: str
    confidence: float
    verified_date: datetime
    verification_method: str

@dataclass
class TechnologyInfo:
    """Comprehensive information about a technology"""
    name: str
    created_by: str
    first_release: str
    current_version: str
    language: str
    license_type: str
    repository: str
    official_docs: str
    facts: List[TechnologyFact] = field(default_factory=list)
    common_misconceptions: List[str] = field(default_factory=list)
    related_technologies: List[str] = field(default_factory=list)
    ecosystem: Dict[str, Any] = field(default_factory=dict)

class SimpleKnowledgeBase:
    """Simple knowledge base for testing"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, TechnologyInfo]:
        """Initialize knowledge base with basic technologies"""
        return {
            "react": TechnologyInfo(
                name="React",
                created_by="Facebook (Meta)",
                first_release="2013-05-29",
                current_version="18.2.0",
                language="JavaScript",
                license_type="MIT",
                repository="https://github.com/facebook/react",
                official_docs="https://react.dev/",
                facts=[
                    TechnologyFact(
                        fact="React is a JavaScript library for building user interfaces",
                        source="Official React Documentation",
                        confidence=0.95,
                        verified_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
                        verification_method="official_docs"
                    ),
                    TechnologyFact(
                        fact="React uses a virtual DOM for efficient updates",
                        source="Official React Documentation",
                        confidence=0.95,
                        verified_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
                        verification_method="official_docs"
                    )
                ],
                common_misconceptions=[
                    "React is a framework (it's a library)",
                    "Class components are obsolete (still supported)"
                ],
                related_technologies=["JavaScript", "TypeScript", "Next.js"],
                ecosystem={
                    "state_management": ["Redux", "Zustand", "MobX"],
                    "routing": ["React Router", "Reach Router"],
                    "styling": ["Styled Components", "Emotion", "Tailwind CSS"]
                }
            ),
            "vue": TechnologyInfo(
                name="Vue.js",
                created_by="Evan You",
                first_release="2014-02",
                current_version="3.4.0",
                language="JavaScript",
                license_type="MIT",
                repository="https://github.com/vuejs/vue",
                official_docs="https://vuejs.org/",
                facts=[
                    TechnologyFact(
                        fact="Vue.js is a progressive JavaScript framework",
                        source="Official Vue.js Documentation",
                        confidence=0.95,
                        verified_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
                        verification_method="official_docs"
                    ),
                    TechnologyFact(
                        fact="Vue.js was created by Evan You",
                        source="Official Vue.js Documentation",
                        confidence=0.95,
                        verified_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
                        verification_method="official_docs"
                    )
                ],
                common_misconceptions=[
                    "Vue is not suitable for large applications",
                    "Vue is slower than React"
                ],
                related_technologies=["JavaScript", "TypeScript", "Nuxt.js"],
                ecosystem={
                    "state_management": ["Vuex", "Pinia"],
                    "routing": ["Vue Router"],
                    "build_tools": ["Vite", "Vue CLI"]
                }
            )
        }
    
    def verify_claim(self, claim: str, technology: str) -> Dict[str, Any]:
        """Verify a claim against the knowledge base"""
        
        if technology not in self.knowledge_base:
            return {
                "verified": False,
                "confidence": 0.0,
                "message": f"Technology '{technology}' not found in knowledge base"
            }
        
        tech_info = self.knowledge_base[technology]
        claim_lower = claim.lower()
        
        # Search for matching facts
        for fact in tech_info.facts:
            if fact.fact.lower() in claim_lower or claim_lower in fact.fact.lower():
                return {
                    "verified": True,
                    "confidence": fact.confidence,
                    "fact": fact.fact,
                    "source": fact.source,
                    "verification_method": fact.verification_method
                }
        
        return {
            "verified": False,
            "confidence": 0.0,
            "message": f"No matching facts found for claim about {technology}"
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get knowledge base summary"""
        return {
            "total_technologies": len(self.knowledge_base),
            "total_facts": sum(len(tech.facts) for tech in self.knowledge_base.values()),
            "technologies": list(self.knowledge_base.keys())
        }

def main():
    """Test the simple knowledge base"""
    print("📚 Simple Knowledge Base Test")
    print("=" * 40)
    
    kb = SimpleKnowledgeBase()
    
    # Test verification
    test_claims = [
        ("React is a JavaScript library", "react"),
        ("Vue was created by Evan You", "vue"),
        ("React uses a virtual DOM", "react"),
        ("Vue is a progressive framework", "vue"),
        ("Invalid claim", "react")
    ]
    
    print("🔍 Testing Fact Verification:")
    for claim, tech in test_claims:
        result = kb.verify_claim(claim, tech)
        status = "✅" if result["verified"] else "❌"
        print(f"{status} {tech}: {claim}")
        if result["verified"]:
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Source: {result['source']}")
        else:
            print(f"   Issue: {result['message']}")
    
    # Get summary
    summary = kb.get_summary()
    print(f"\n📊 Knowledge Base Summary:")
    print(f"   Technologies: {summary['total_technologies']}")
    print(f"   Facts: {summary['total_facts']}")
    print(f"   Technologies: {', '.join(summary['technologies'])}")
    
    print("\n🎉 Simple knowledge base test completed successfully!")

if __name__ == "__main__":
    main()
