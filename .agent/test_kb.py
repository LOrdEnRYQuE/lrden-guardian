#!/usr/bin/env python3
import sys
sys.path.insert(0, 'core')

try:
    from enhanced_knowledge_base import EnhancedKnowledgeBase
    print("✅ Enhanced Knowledge Base loaded successfully!")
    
    kb = EnhancedKnowledgeBase()
    print(f"📚 Technologies: {len(kb.knowledge_base)}")
    print(f"📊 Total Facts: {sum(len(tech.facts) for tech in kb.knowledge_base.values())}")
    
    # Test verification
    result = kb.verify_claim("React is a JavaScript library", "react")
    print(f"🔍 Test verification: {result['verified']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
