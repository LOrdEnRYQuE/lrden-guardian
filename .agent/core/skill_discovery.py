#!/usr/bin/env python3
"""
Dynamic Skill Discovery and Loading System - Enhanced VS Code Agent
====================================================================

Automatically discovers, validates, and loads skills based on context analysis.
Supports skill dependency resolution, versioning, and runtime optimization.

Features:
- Auto-discovery of available skills
- Context-aware skill loading
- Dependency resolution
- Performance optimization
- Skill validation and health checks
"""

import os
import json
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import re

@dataclass
class SkillMetadata:
    """Metadata for a discovered skill"""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    priority: int = 0
    category: str = ""
    file_count: int = 0
    last_modified: datetime = field(default_factory=datetime.now)
    skill_path: Path = field(default_factory=Path)
    manifest_hash: str = ""
    
    def __post_init__(self):
        if isinstance(self.last_modified, str):
            self.last_modified = datetime.fromisoformat(self.last_modified)

@dataclass
class SkillContext:
    """Context analysis result for skill matching"""
    request_type: str
    keywords: Set[str]
    technologies: Set[str]
    frameworks: Set[str]
    file_types: Set[str]
    complexity: str  # simple, moderate, complex
    domain: str  # frontend, backend, devops, etc.
    intent: str  # create, fix, analyze, optimize

class SkillDiscovery:
    """Dynamic skill discovery and loading system"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.skills_dir = agent_root / "skills"
        self.skills_registry: Dict[str, SkillMetadata] = {}
        self.context_cache: Dict[str, List[str]] = {}
        self.load_order_cache: Dict[str, List[str]] = {}
        
    def discover_all_skills(self) -> Dict[str, SkillMetadata]:
        """Discover all available skills in the skills directory"""
        if not self.skills_dir.exists():
            print(f"Skills directory not found: {self.skills_dir}")
            return {}
        
        skills = {}
        
        # Scan skills directory
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill = self._analyze_skill(skill_path)
                if skill:
                    skills[skill.name] = skill
            elif skill_path.name == "doc.md" or skill_path.suffix == ".md":
                # Handle standalone skill documentation
                skill = self._analyze_standalone_skill(skill_path)
                if skill:
                    skills[skill.name] = skill
        
        self.skills_registry = skills
        return skills
    
    def _analyze_skill(self, skill_path: Path) -> Optional[SkillMetadata]:
        """Analyze a skill directory and extract metadata"""
        
        # Look for SKILL.md file
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            return None
        
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # Parse frontmatter
            frontmatter, content_body = self._parse_frontmatter(content)
            
            # Extract metadata
            name = frontmatter.get('name', skill_path.name)
            description = frontmatter.get('description', '')
            version = frontmatter.get('version', '1.0.0')
            author = frontmatter.get('author', '')
            tags = frontmatter.get('tags', [])
            dependencies = frontmatter.get('dependencies', [])
            conflicts = frontmatter.get('conflicts', [])
            priority = frontmatter.get('priority', 0)
            category = frontmatter.get('category', self._infer_category(skill_path, content_body))
            
            # Count files
            file_count = len(list(skill_path.rglob('*'))) if skill_path.is_dir() else 1
            
            # Get modification time
            last_modified = datetime.fromtimestamp(skill_path.stat().st_mtime)
            
            # Calculate manifest hash
            manifest_hash = self._calculate_manifest_hash(skill_path)
            
            return SkillMetadata(
                name=name,
                description=description,
                version=version,
                author=author,
                tags=tags if isinstance(tags, list) else [tags],
                dependencies=dependencies if isinstance(dependencies, list) else [dependencies],
                conflicts=conflicts if isinstance(conflicts, list) else [conflicts],
                priority=priority,
                category=category,
                file_count=file_count,
                last_modified=last_modified,
                skill_path=skill_path,
                manifest_hash=manifest_hash
            )
            
        except Exception as e:
            print(f"Error analyzing skill {skill_path}: {e}")
            return None
    
    def _analyze_standalone_skill(self, skill_file: Path) -> Optional[SkillMetadata]:
        """Analyze a standalone skill documentation file"""
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # Extract basic info from filename and content
            name = skill_file.stem.replace('-', '_')
            description = self._extract_description_from_content(content)
            
            return SkillMetadata(
                name=name,
                description=description,
                version="1.0.0",
                category=self._infer_category(skill_file, content),
                file_count=1,
                last_modified=datetime.fromtimestamp(skill_file.stat().st_mtime),
                skill_path=skill_file,
                manifest_hash=hashlib.md5(content.encode()).hexdigest()
            )
            
        except Exception as e:
            print(f"Error analyzing standalone skill {skill_file}: {e}")
            return None
    
    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                end_index = content.find('---', 3)
                if end_index != -1:
                    frontmatter_str = content[3:end_index].strip()
                    body = content[end_index + 3:].strip()
                    frontmatter = yaml.safe_load(frontmatter_str) or {}
                    return frontmatter, body
            except yaml.YAMLError:
                pass
        
        return {}, content
    
    def _extract_description_from_content(self, content: str) -> str:
        """Extract description from content"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                continue  # Skip title
            elif line.startswith('> '):
                return line[2:].strip()
            elif line and not line.startswith('#') and not line.startswith('```'):
                return line[:100] + ('...' if len(line) > 100 else '')
        return "No description available"
    
    def _infer_category(self, skill_path: Path, content: str) -> str:
        """Infer skill category from path and content"""
        path_lower = str(skill_path).lower()
        content_lower = content.lower()
        
        category_keywords = {
            'frontend': ['react', 'vue', 'angular', 'css', 'tailwind', 'ui', 'frontend', 'web'],
            'backend': ['api', 'server', 'node', 'python', 'nest', 'backend', 'database'],
            'devops': ['docker', 'deploy', 'ci', 'cd', 'kubernetes', 'devops', 'infrastructure'],
            'mobile': ['mobile', 'ios', 'android', 'react-native', 'flutter'],
            'testing': ['test', 'jest', 'playwright', 'cypress', 'testing'],
            'security': ['security', 'vulnerability', 'auth', 'owasp', 'penetration'],
            'performance': ['performance', 'optimization', 'speed', 'lighthouse'],
            'architecture': ['architecture', 'design', 'pattern', 'structure'],
            'tools': ['tools', 'cli', 'bash', 'powershell', 'automation']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in path_lower or keyword in content_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _calculate_manifest_hash(self, skill_path: Path) -> str:
        """Calculate hash of skill manifest files"""
        hash_content = ""
        
        if skill_path.is_dir():
            # Include SKILL.md and other key files
            for file_name in ['SKILL.md', 'README.md', 'package.json', 'requirements.txt']:
                file_path = skill_path / file_name
                if file_path.exists():
                    hash_content += file_path.read_text(encoding='utf-8')
        else:
            # Single file skill
            hash_content += skill_path.read_text(encoding='utf-8')
        
        return hashlib.md5(hash_content.encode()).hexdigest()
    
    def analyze_request_context(self, request: str) -> SkillContext:
        """Analyze user request to determine context"""
        request_lower = request.lower()
        
        # Extract keywords
        keywords = set(re.findall(r'\b\w+\b', request_lower))
        
        # Identify technologies
        tech_patterns = {
            'react': r'\breact\b|\bjsx\b|\btsx\b',
            'vue': r'\bvue\b',
            'angular': r'\bangular\b',
            'node': r'\bnode\b|\bnpm\b|\byarn\b',
            'python': r'\bpython\b|\bdjango\b|\bflask\b',
            'docker': r'\bdocker\b|\bcontainer\b',
            'kubernetes': r'\bkubernetes\b|\bk8s\b',
            'typescript': r'\btypescript\b|\bts\b',
            'javascript': r'\bjavascript\b|\bjs\b'
        }
        
        technologies = set()
        for tech, pattern in tech_patterns.items():
            if re.search(pattern, request_lower):
                technologies.add(tech)
        
        # Identify frameworks
        frameworks = set()
        framework_patterns = {
            'express': r'\bexpress\b',
            'fastapi': r'\bfastapi\b',
            'nest': r'\bnest\b|\bnestjs\b',
            'next': r'\bnext\b|\bnextjs\b',
            'tailwind': r'\btailwind\b',
            'prisma': r'\bprisma\b'
        }
        
        for framework, pattern in framework_patterns.items():
            if re.search(pattern, request_lower):
                frameworks.add(framework)
        
        # Identify file types
        file_types = set()
        file_extensions = ['.js', '.ts', '.jsx', '.tsx', '.py', '.html', '.css', '.json', '.md']
        for ext in file_extensions:
            if ext in request_lower:
                file_types.add(ext)
        
        # Determine complexity
        complexity_indicators = {
            'simple': ['fix', 'add', 'change', 'update', 'simple'],
            'moderate': ['implement', 'create', 'build', 'develop'],
            'complex': ['architecture', 'system', 'comprehensive', 'full-stack', 'enterprise']
        }
        
        complexity = 'moderate'  # default
        for level, indicators in complexity_indicators.items():
            if any(indicator in request_lower for indicator in indicators):
                complexity = level
                break
        
        # Determine domain
        domain_keywords = {
            'frontend': ['ui', 'frontend', 'component', 'page', 'interface'],
            'backend': ['api', 'backend', 'server', 'database'],
            'devops': ['deploy', 'docker', 'ci', 'cd'],
            'mobile': ['mobile', 'app', 'ios', 'android'],
            'testing': ['test', 'testing', 'spec'],
            'security': ['security', 'auth', 'vulnerability']
        }
        
        domain = 'general'
        for d, keywords in domain_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                domain = d
                break
        
        # Determine intent
        intent_patterns = {
            'create': r'\bcreate\b|\bbuild\b|\bimplement\b|\bdevelop\b',
            'fix': r'\bfix\b|\bdebug\b|\bresolve\b|\berror\b',
            'analyze': r'\banalyze\b|\breview\b|\baudit\b|\bcheck\b',
            'optimize': r'\boptimize\b|\bimprove\b|\benhance\b|\bperformance\b'
        }
        
        intent = 'general'
        for intent_type, pattern in intent_patterns.items():
            if re.search(pattern, request_lower):
                intent = intent_type
                break
        
        return SkillContext(
            request_type=self._classify_request_type(request),
            keywords=keywords,
            technologies=technologies,
            frameworks=frameworks,
            file_types=file_types,
            complexity=complexity,
            domain=domain,
            intent=intent
        )
    
    def _classify_request_type(self, request: str) -> str:
        """Classify the type of request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['what', 'how', 'explain', 'describe']):
            return 'question'
        elif any(word in request_lower for word in ['analyze', 'list', 'show', 'overview']):
            return 'survey'
        elif any(word in request_lower for word in ['fix', 'add', 'change', 'update']) and len(request.split()) < 10:
            return 'simple_code'
        elif any(word in request_lower for word in ['build', 'create', 'implement', 'refactor']):
            return 'complex_code'
        elif any(word in request_lower for word in ['design', 'ui', 'page', 'dashboard']):
            return 'design'
        elif request.startswith('/'):
            return 'slash_command'
        
        return 'general'
    
    def find_relevant_skills(self, context: SkillContext, limit: int = 5) -> List[Tuple[str, float]]:
        """Find skills relevant to the given context"""
        if not self.skills_registry:
            self.discover_all_skills()
        
        scored_skills = []
        
        for skill_name, skill in self.skills_registry.items():
            score = self._calculate_relevance_score(skill, context)
            if score > 0:
                scored_skills.append((skill_name, score))
        
        # Sort by score (descending) and return top results
        scored_skills.sort(key=lambda x: x[1], reverse=True)
        return scored_skills[:limit]
    
    def _calculate_relevance_score(self, skill: SkillMetadata, context: SkillContext) -> float:
        """Calculate relevance score for a skill given the context"""
        score = 0.0
        
        # Category matching
        if skill.category == context.domain:
            score += 2.0
        elif skill.category == 'general':
            score += 0.5
        
        # Keyword matching in description and tags
        skill_text = f"{skill.description} {' '.join(skill.tags)}".lower()
        
        for keyword in context.keywords:
            if keyword in skill_text:
                score += 0.5
        
        # Technology matching
        for tech in context.technologies:
            if tech in skill_text:
                score += 1.0
        
        # Framework matching
        for framework in context.frameworks:
            if framework in skill_text:
                score += 1.0
        
        # Intent matching
        if context.intent in skill.tags:
            score += 1.5
        
        # Priority bonus
        try:
            priority_value = float(skill.priority) if isinstance(skill.priority, (int, float, str)) else 0
            score += priority_value * 0.1
        except (ValueError, TypeError):
            score += 0  # Default to 0 if priority can't be converted
        
        # Complexity matching
        try:
            priority_value = float(skill.priority) if isinstance(skill.priority, (int, float, str)) else 0
            if context.complexity == 'simple' and priority_value <= 3:
                score += 0.5
            elif context.complexity == 'complex' and priority_value >= 7:
                score += 0.5
        except (ValueError, TypeError):
            pass  # Skip complexity matching if priority can't be converted
        
        return score
    
    def resolve_dependencies(self, skill_names: List[str]) -> List[str]:
        """Resolve skill dependencies in correct order"""
        resolved = []
        visited = set()
        
        def visit(skill_name: str):
            if skill_name in visited:
                return
            visited.add(skill_name)
            
            if skill_name in self.skills_registry:
                skill = self.skills_registry[skill_name]
                for dep in skill.dependencies:
                    visit(dep)
            
            resolved.append(skill_name)
        
        for skill_name in skill_names:
            visit(skill_name)
        
        return resolved
    
    def validate_skill_health(self, skill_name: str) -> Dict[str, Any]:
        """Validate the health of a skill"""
        if skill_name not in self.skills_registry:
            return {"status": "not_found", "issues": ["Skill not found in registry"]}
        
        skill = self.skills_registry[skill_name]
        issues = []
        
        # Check if skill path exists
        if not skill.skill_path.exists():
            issues.append("Skill path does not exist")
        
        # Check for required files
        if skill.skill_path.is_dir():
            skill_file = skill.skill_path / "SKILL.md"
            if not skill_file.exists():
                issues.append("Missing SKILL.md file")
        
        # Check dependencies
        for dep in skill.dependencies:
            if dep not in self.skills_registry:
                issues.append(f"Missing dependency: {dep}")
        
        # Check for conflicts
        for conflict in skill.conflicts:
            if conflict in self.skills_registry:
                issues.append(f"Conflict with skill: {conflict}")
        
        return {
            "status": "healthy" if not issues else "unhealthy",
            "issues": issues,
            "metadata": {
                "name": skill.name,
                "version": skill.version,
                "category": skill.category,
                "file_count": skill.file_count
            }
        }
    
    def get_skills_summary(self) -> Dict[str, Any]:
        """Get summary of all discovered skills"""
        if not self.skills_registry:
            self.discover_all_skills()
        
        categories = {}
        total_skills = len(self.skills_registry)
        
        for skill in self.skills_registry.values():
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill.name)
        
        return {
            "total_skills": total_skills,
            "categories": categories,
            "skills": {name: {
                "description": skill.description,
                "category": skill.category,
                "priority": skill.priority,
                "dependencies": skill.dependencies
            } for name, skill in self.skills_registry.items()}
        }

def main():
    """Test the skill discovery system"""
    agent_root = Path.cwd() / ".agent"
    discovery = SkillDiscovery(agent_root)
    
    # Discover skills
    skills = discovery.discover_all_skills()
    print(f"Discovered {len(skills)} skills")
    
    # Test context analysis
    test_request = "Create a React component with TypeScript and Tailwind CSS"
    context = discovery.analyze_request_context(test_request)
    
    print(f"\nContext Analysis:")
    print(f"Request Type: {context.request_type}")
    print(f"Domain: {context.domain}")
    print(f"Technologies: {context.technologies}")
    print(f"Frameworks: {context.frameworks}")
    print(f"Complexity: {context.complexity}")
    print(f"Intent: {context.intent}")
    
    # Find relevant skills
    relevant_skills = discovery.find_relevant_skills(context)
    print(f"\nRelevant Skills:")
    for skill_name, score in relevant_skills:
        print(f"  {skill_name}: {score:.2f}")

if __name__ == "__main__":
    main()
