#!/usr/bin/env python3
"""
AI-Powered Routing Engine - Enhanced VS Code Agent System
========================================================

Intelligent agent and skill selection based on context analysis.
Eliminates manual agent/skill selection through AI-powered routing.

Features:
- Automatic agent selection
- Multi-agent orchestration
- Context-aware skill chaining
- Performance optimization
- Learning and adaptation
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math

from skill_discovery import SkillDiscovery, SkillContext
from ide_detector import IDEDetector

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

class DomainType(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    MOBILE = "mobile"
    DEVOPS = "devops"
    SECURITY = "security"
    TESTING = "testing"
    DATA = "data"
    ARCHITECTURE = "architecture"
    GENERAL = "general"

@dataclass
class AgentProfile:
    """Profile of an agent with capabilities and expertise"""
    name: str
    description: str
    domains: List[DomainType]
    skills: List[str]
    complexity_level: TaskComplexity
    collaboration_score: float  # 0-1, how well they work with others
    expertise_score: float  # 0-1, depth of expertise
    file_path: Path
    priority: int = 0
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.domains, str):
            self.domains = [DomainType(d) for d in self.domains]
        if isinstance(self.complexity_level, str):
            self.complexity_level = TaskComplexity(self.complexity_level)

@dataclass
class RoutingDecision:
    """Routing decision with confidence score"""
    primary_agent: str
    secondary_agents: List[str]
    skills_to_load: List[str]
    confidence: float
    reasoning: str
    execution_plan: List[str]
    estimated_time: int  # in minutes

class AIRouter:
    """AI-powered routing engine for intelligent agent/skill selection"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.agents_dir = agent_root / "agents"
        self.skill_discovery = SkillDiscovery(agent_root)
        self.ide_detector = IDEDetector()
        
        self.agent_profiles: Dict[str, AgentProfile] = {}
        self.routing_history: List[Dict] = []
        self.performance_cache: Dict[str, float] = {}
        
        # Load agent profiles
        self._load_agent_profiles()
    
    def _load_agent_profiles(self):
        """Load and analyze all agent profiles"""
        if not self.agents_dir.exists():
            print(f"Agents directory not found: {self.agents_dir}")
            return
        
        for agent_file in self.agents_dir.glob("*.md"):
            try:
                profile = self._analyze_agent_file(agent_file)
                if profile:
                    self.agent_profiles[profile.name] = profile
            except Exception as e:
                print(f"Error loading agent {agent_file}: {e}")
    
    def _analyze_agent_file(self, agent_file: Path) -> Optional[AgentProfile]:
        """Analyze an agent file and extract profile information"""
        try:
            content = agent_file.read_text(encoding='utf-8')
            
            # Parse frontmatter
            frontmatter, content_body = self._parse_frontmatter(content)
            
            name = frontmatter.get('name', agent_file.stem)
            description = frontmatter.get('description', '')
            skills = frontmatter.get('skills', [])
            priority = frontmatter.get('priority', 0)
            tags = frontmatter.get('tags', [])
            
            # Analyze content to determine domains and complexity
            domains = self._infer_domains(content_body)
            complexity = self._infer_complexity(content_body)
            
            # Calculate scores based on content analysis
            expertise_score = self._calculate_expertise_score(content_body, skills)
            collaboration_score = self._calculate_collaboration_score(content_body)
            
            return AgentProfile(
                name=name,
                description=description,
                domains=domains,
                skills=skills if isinstance(skills, list) else [skills],
                complexity_level=complexity,
                collaboration_score=collaboration_score,
                expertise_score=expertise_score,
                file_path=agent_file,
                priority=priority,
                tags=tags if isinstance(tags, list) else [tags]
            )
            
        except Exception as e:
            print(f"Error analyzing agent {agent_file}: {e}")
            return None
    
    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                end_index = content.find('---', 3)
                if end_index != -1:
                    frontmatter_str = content[3:end_index].strip()
                    body = content[end_index + 3:].strip()
                    import yaml
                    frontmatter = yaml.safe_load(frontmatter_str) or {}
                    return frontmatter, body
            except:
                pass
        
        return {}, content
    
    def _infer_domains(self, content: str) -> List[DomainType]:
        """Infer agent domains from content"""
        content_lower = content.lower()
        domains = []
        
        domain_keywords = {
            DomainType.FRONTEND: ['frontend', 'ui', 'react', 'vue', 'angular', 'css', 'tailwind', 'component'],
            DomainType.BACKEND: ['backend', 'api', 'server', 'node', 'python', 'database', 'prisma'],
            DomainType.FULLSTACK: ['fullstack', 'full-stack', 'end-to-end', 'complete'],
            DomainType.MOBILE: ['mobile', 'ios', 'android', 'react-native', 'flutter'],
            DomainType.DEVOPS: ['devops', 'docker', 'deploy', 'ci', 'cd', 'kubernetes'],
            DomainType.SECURITY: ['security', 'vulnerability', 'auth', 'penetration', 'audit'],
            DomainType.TESTING: ['test', 'testing', 'jest', 'playwright', 'cypress'],
            DomainType.DATA: ['data', 'analytics', 'database', 'sql', 'nosql'],
            DomainType.ARCHITECTURE: ['architecture', 'design', 'pattern', 'structure', 'system']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                domains.append(domain)
        
        return domains if domains else [DomainType.GENERAL]
    
    def _infer_complexity(self, content: str) -> TaskComplexity:
        """Infer agent complexity level from content"""
        content_lower = content.lower()
        
        complexity_indicators = {
            TaskComplexity.SIMPLE: ['simple', 'basic', 'quick', 'minor'],
            TaskComplexity.MODERATE: ['moderate', 'standard', 'typical', 'regular'],
            TaskComplexity.COMPLEX: ['complex', 'advanced', 'comprehensive', 'detailed'],
            TaskComplexity.ENTERPRISE: ['enterprise', 'production', 'scalable', 'mission-critical']
        }
        
        scores = {}
        for complexity, indicators in complexity_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            scores[complexity] = score
        
        # Return complexity with highest score
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _calculate_expertise_score(self, content: str, skills: List[str]) -> float:
        """Calculate expertise score based on content depth and skills"""
        base_score = 0.5
        
        # More skills = higher expertise (diminishing returns)
        skill_score = min(len(skills) / 10, 1.0) * 0.3
        
        # Content length indicates depth (up to a point)
        length_score = min(len(content) / 5000, 1.0) * 0.2
        
        return min(base_score + skill_score + length_score, 1.0)
    
    def _calculate_collaboration_score(self, content: str) -> float:
        """Calculate collaboration score based on content analysis"""
        content_lower = content.lower()
        
        collaboration_keywords = [
            'coordinate', 'orchestrate', 'collaborate', 'team', 'multi-agent',
            'integration', 'communication', 'workflow', 'pipeline'
        ]
        
        keyword_score = sum(1 for keyword in collaboration_keywords if keyword in content_lower)
        keyword_score = min(keyword_score / len(collaboration_keywords), 1.0) * 0.7
        
        # Check for agent coordination patterns
        coordination_patterns = [
            r'\bcoordinate\b.*\bagent\b',
            r'\bmultiple\b.*\bagents?',
            r'\bteam\b.*\bwork\b'
        ]
        
        pattern_score = sum(1 for pattern in coordination_patterns if re.search(pattern, content_lower))
        pattern_score = min(pattern_score / len(coordination_patterns), 1.0) * 0.3
        
        return keyword_score + pattern_score
    
    def route_request(self, request: str, context: Optional[SkillContext] = None) -> RoutingDecision:
        """Route a request to the best agent(s) and skills"""
        
        # Analyze context if not provided
        if not context:
            context = self.skill_discovery.analyze_request_context(request)
        
        # Determine task complexity
        complexity = self._determine_task_complexity(request, context)
        
        # Find candidate agents
        candidates = self._find_candidate_agents(context, complexity)
        
        # Select primary agent
        primary_agent = self._select_primary_agent(candidates, context, complexity)
        
        # Select secondary agents if needed
        secondary_agents = self._select_secondary_agents(primary_agent, candidates, context, complexity)
        
        # Find relevant skills
        relevant_skills = self.skill_discovery.find_relevant_skills(context)
        skills_to_load = self.skill_discovery.resolve_dependencies([skill for skill, _ in relevant_skills])
        
        # Calculate confidence
        confidence = self._calculate_routing_confidence(primary_agent, secondary_agents, context)
        
        # Generate execution plan
        execution_plan = self._generate_execution_plan(primary_agent, secondary_agents, skills_to_load, context)
        
        # Estimate time
        estimated_time = self._estimate_execution_time(primary_agent, secondary_agents, skills_to_load, complexity)
        
        # Generate reasoning
        reasoning = self._generate_routing_reasoning(primary_agent, secondary_agents, context, complexity)
        
        # Create routing decision
        decision = RoutingDecision(
            primary_agent=primary_agent,
            secondary_agents=secondary_agents,
            skills_to_load=skills_to_load,
            confidence=confidence,
            reasoning=reasoning,
            execution_plan=execution_plan,
            estimated_time=estimated_time
        )
        
        # Cache performance
        self._cache_routing_performance(request, decision)
        
        return decision
    
    def _determine_task_complexity(self, request: str, context: SkillContext) -> TaskComplexity:
        """Determine task complexity from request and context"""
        
        # Base complexity from context
        complexity_mapping = {
            'simple': TaskComplexity.SIMPLE,
            'moderate': TaskComplexity.MODERATE,
            'complex': TaskComplexity.COMPLEX
        }
        
        base_complexity = complexity_mapping.get(context.complexity, TaskComplexity.MODERATE)
        
        # Adjust based on request characteristics
        request_lower = request.lower()
        
        # Enterprise indicators
        enterprise_keywords = ['enterprise', 'production', 'scalable', 'mission-critical', 'large-scale']
        if any(keyword in request_lower for keyword in enterprise_keywords):
            return TaskComplexity.ENTERPRISE
        
        # Multi-domain indicators
        domain_count = len(context.technologies) + len(context.frameworks)
        if domain_count > 3:
            if base_complexity == TaskComplexity.SIMPLE:
                return TaskComplexity.MODERATE
            elif base_complexity == TaskComplexity.MODERATE:
                return TaskComplexity.COMPLEX
            else:
                return TaskComplexity.ENTERPRISE
        
        return base_complexity
    
    def _find_candidate_agents(self, context: SkillContext, complexity: TaskComplexity) -> List[Tuple[str, float]]:
        """Find candidate agents with relevance scores"""
        candidates = []
        
        for agent_name, agent in self.agent_profiles.items():
            score = self._calculate_agent_relevance(agent, context, complexity)
            if score > 0:
                candidates.append((agent_name, score))
        
        # Sort by relevance score
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates
    
    def _calculate_agent_relevance(self, agent: AgentProfile, context: SkillContext, complexity: TaskComplexity) -> float:
        """Calculate relevance score for an agent"""
        score = 0.0
        
        # Domain matching
        domain_match = any(domain.value == context.domain for domain in agent.domains)
        if domain_match:
            score += 3.0
        elif DomainType.GENERAL in agent.domains:
            score += 1.0
        elif DomainType.FULLSTACK in agent.domains and context.domain in ['frontend', 'backend']:
            score += 2.0
        
        # Skill matching
        agent_skills_text = ' '.join(agent.skills).lower()
        for tech in context.technologies:
            if tech in agent_skills_text:
                score += 1.5
        for framework in context.frameworks:
            if framework in agent_skills_text:
                score += 1.5
        
        # Complexity matching
        complexity_levels = {
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 3,
            TaskComplexity.ENTERPRISE: 4
        }
        
        agent_level = complexity_levels[agent.complexity_level]
        required_level = complexity_levels[complexity]
        
        if agent_level >= required_level:
            score += 1.0
        else:
            score -= 0.5  # Penalty for insufficient complexity level
        
        # Expertise bonus
        score += agent.expertise_score * 0.5
        
        # Priority bonus
        try:
            priority_value = float(agent.priority) if isinstance(agent.priority, (int, float, str)) else 0
            score += priority_value * 0.1
        except (ValueError, TypeError):
            score += 0  # Default to 0 if priority can't be converted
        
        return max(score, 0.0)
    
    def _select_primary_agent(self, candidates: List[Tuple[str, float]], context: SkillContext, complexity: TaskComplexity) -> str:
        """Select the primary agent from candidates"""
        if not candidates:
            return "orchestrator"  # Fallback to orchestrator
        
        # Get top candidate
        primary_agent, score = candidates[0]
        
        # If confidence is low, use orchestrator
        if score < 1.0 and complexity in [TaskComplexity.COMPLEX, TaskComplexity.ENTERPRISE]:
            return "orchestrator"
        
        return primary_agent
    
    def _select_secondary_agents(self, primary_agent: str, candidates: List[Tuple[str, float]], context: SkillContext, complexity: TaskComplexity) -> List[str]:
        """Select secondary agents for collaboration"""
        secondary = []
        
        # For complex tasks, add more agents
        max_secondary = {
            TaskComplexity.SIMPLE: 0,
            TaskComplexity.MODERATE: 1,
            TaskComplexity.COMPLEX: 2,
            TaskComplexity.ENTERPRISE: 3
        }.get(complexity, 1)
        
        # Skip primary agent
        filtered_candidates = [(name, score) for name, score in candidates if name != primary_agent]
        
        # Select agents with different domains for comprehensive coverage
        primary_domains = set(self.agent_profiles[primary_agent].domains) if primary_agent in self.agent_profiles else set()
        
        for agent_name, score in filtered_candidates[:max_secondary * 2]:  # Get more candidates to choose from
            if len(secondary) >= max_secondary:
                break
            
            if agent_name in self.agent_profiles:
                agent = self.agent_profiles[agent_name]
                # Prefer agents with complementary domains
                agent_domains = set(agent.domains)
                if not agent_domains.intersection(primary_domains) or DomainType.GENERAL in agent_domains:
                    secondary.append(agent_name)
        
        return secondary
    
    def _calculate_routing_confidence(self, primary_agent: str, secondary_agents: List[str], context: SkillContext) -> float:
        """Calculate confidence in routing decision"""
        confidence = 0.5  # Base confidence
        
        # Primary agent confidence
        if primary_agent in self.agent_profiles:
            agent = self.agent_profiles[primary_agent]
            confidence += agent.expertise_score * 0.3
        
        # Secondary agents boost confidence
        confidence += len(secondary_agents) * 0.1
        
        # Context clarity
        if context.domain != 'general':
            confidence += 0.1
        if context.technologies or context.frameworks:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_execution_plan(self, primary_agent: str, secondary_agents: List[str], skills: List[str], context: SkillContext) -> List[str]:
        """Generate execution plan"""
        plan = []
        
        # Initial analysis
        plan.append(f"1. Load context and analyze request: {context.intent}")
        
        # Load skills
        if skills:
            plan.append(f"2. Load skills: {', '.join(skills[:3])}" + ("..." if len(skills) > 3 else ""))
        
        # Primary agent work
        plan.append(f"3. Primary agent ({primary_agent}) executes main task")
        
        # Secondary agent collaboration
        for i, agent in enumerate(secondary_agents, 1):
            plan.append(f"4.{i}. Secondary agent ({agent}) provides specialized input")
        
        # Final synthesis
        if secondary_agents:
            plan.append(f"5. Synthesize results and generate final output")
        else:
            plan.append(f"4. Generate final output")
        
        return plan
    
    def _estimate_execution_time(self, primary_agent: str, secondary_agents: List[str], skills: List[str], complexity: TaskComplexity) -> int:
        """Estimate execution time in minutes"""
        base_times = {
            TaskComplexity.SIMPLE: 5,
            TaskComplexity.MODERATE: 15,
            TaskComplexity.COMPLEX: 30,
            TaskComplexity.ENTERPRISE: 60
        }
        
        base_time = base_times.get(complexity, 15)
        
        # Add time for skills
        skill_time = len(skills) * 2
        
        # Add time for secondary agents
        collaboration_time = len(secondary_agents) * 5
        
        return base_time + skill_time + collaboration_time
    
    def _generate_routing_reasoning(self, primary_agent: str, secondary_agents: List[str], context: SkillContext, complexity: TaskComplexity) -> str:
        """Generate human-readable reasoning for routing decision"""
        reasoning_parts = []
        
        # Primary agent reasoning
        if primary_agent in self.agent_profiles:
            agent = self.agent_profiles[primary_agent]
            reasoning_parts.append(f"Selected {primary_agent} as primary agent due to expertise in {', '.join(d.value for d in agent.domains)}")
        
        # Complexity reasoning
        reasoning_parts.append(f"Task complexity assessed as {complexity.value}")
        
        # Domain reasoning
        if context.domain != 'general':
            reasoning_parts.append(f"Domain identified as {context.domain}")
        
        # Technology reasoning
        if context.technologies:
            reasoning_parts.append(f"Technologies involved: {', '.join(context.technologies)}")
        
        # Collaboration reasoning
        if secondary_agents:
            reasoning_parts.append(f"Added {len(secondary_agents)} secondary agents for comprehensive coverage")
        
        return "; ".join(reasoning_parts)
    
    def _cache_routing_performance(self, request: str, decision: RoutingDecision):
        """Cache routing performance for learning"""
        self.routing_history.append({
            "timestamp": datetime.now().isoformat(),
            "request": request[:100],  # Truncate for privacy
            "primary_agent": decision.primary_agent,
            "secondary_agents": decision.secondary_agents,
            "confidence": decision.confidence,
            "skills_count": len(decision.skills_to_load)
        })
        
        # Keep only recent history
        if len(self.routing_history) > 1000:
            self.routing_history = self.routing_history[-1000:]
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing statistics and performance metrics"""
        if not self.routing_history:
            return {"message": "No routing history available"}
        
        # Agent usage statistics
        agent_usage = {}
        for entry in self.routing_history:
            primary = entry["primary_agent"]
            agent_usage[primary] = agent_usage.get(primary, 0) + 1
        
        # Confidence statistics
        confidences = [entry["confidence"] for entry in self.routing_history]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Recent performance
        recent_entries = self.routing_history[-10:]
        recent_avg_confidence = sum(entry["confidence"] for entry in recent_entries) / len(recent_entries)
        
        return {
            "total_routings": len(self.routing_history),
            "agent_usage": agent_usage,
            "average_confidence": avg_confidence,
            "recent_confidence": recent_avg_confidence,
            "available_agents": len(self.agent_profiles),
            "most_used_agent": max(agent_usage.items(), key=lambda x: x[1])[0] if agent_usage else None
        }

def main():
    """Test the AI routing system"""
    agent_root = Path.cwd() / ".agent"
    router = AIRouter(agent_root)
    
    # Test routing
    test_requests = [
        "Create a React component with TypeScript and Tailwind CSS",
        "Build a REST API with Node.js and Express",
        "Set up Docker containerization for a web application",
        "Implement comprehensive security audit for existing codebase"
    ]
    
    for request in test_requests:
        print(f"\nRouting request: {request}")
        decision = router.route_request(request)
        
        print(f"Primary Agent: {decision.primary_agent}")
        print(f"Secondary Agents: {decision.secondary_agents}")
        print(f"Confidence: {decision.confidence:.2f}")
        print(f"Skills: {decision.skills_to_load[:3]}..." if len(decision.skills_to_load) > 3 else f"Skills: {decision.skills_to_load}")
        print(f"Estimated Time: {decision.estimated_time} minutes")
        print(f"Reasoning: {decision.reasoning}")
        print("-" * 50)
    
    # Show statistics
    stats = router.get_routing_statistics()
    print(f"\nRouting Statistics:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
