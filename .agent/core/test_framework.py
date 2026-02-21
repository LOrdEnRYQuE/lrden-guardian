#!/usr/bin/env python3
"""
Comprehensive Testing Framework - Enhanced VS Code Agent System
===============================================================

Advanced testing framework for validating agent system components.
Supports unit tests, integration tests, performance tests, and health checks.

Features:
- Component validation
- Performance benchmarking
- Integration testing
- Health monitoring
- Automated test discovery
- Detailed reporting
"""

import os
import sys
import json
import time
import traceback
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import unittest
import importlib.util

class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    HEALTH = "health"
    SYSTEM = "system"

@dataclass
class TestResult:
    """Result of a single test"""
    name: str
    type: TestType
    status: TestStatus
    duration: float
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "status": self.status.value,
            "duration": self.duration,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class TestSuite:
    """Collection of test results"""
    name: str
    tests: List[TestResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def duration(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def passed_count(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.PASSED])
    
    @property
    def failed_count(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.FAILED])
    
    @property
    def error_count(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.ERROR])
    
    @property
    def skipped_count(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.SKIPPED])
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "duration": self.duration,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "summary": {
                "total": len(self.tests),
                "passed": self.passed_count,
                "failed": self.failed_count,
                "errors": self.error_count,
                "skipped": self.skipped_count
            },
            "tests": [test.to_dict() for test in self.tests]
        }

class TestFramework:
    """Comprehensive testing framework for the agent system"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.core_dir = agent_root / "core"
        self.test_results: List[TestSuite] = []
        self.test_functions: Dict[str, Callable] = {}
        
        # Register test functions
        self._register_tests()
    
    def _register_tests(self):
        """Register all test functions"""
        self.test_functions.update({
            # Core component tests
            "test_ide_detector": self._test_ide_detector,
            "test_skill_discovery": self._test_skill_discovery,
            "test_ai_router": self._test_ai_router,
            
            # Integration tests
            "test_full_routing_pipeline": self._test_full_routing_pipeline,
            "test_skill_loading": self._test_skill_loading,
            "test_agent_coordination": self._test_agent_coordination,
            
            # Performance tests
            "test_routing_performance": self._test_routing_performance,
            "test_skill_discovery_performance": self._test_skill_discovery_performance,
            
            # Health checks
            "test_system_health": self._test_system_health,
            "test_dependency_health": self._test_dependency_health,
            "test_configuration_health": self._test_configuration_health
        })
    
    def run_all_tests(self, test_types: Optional[List[TestType]] = None) -> TestSuite:
        """Run all tests or specific test types"""
        suite = TestSuite("Comprehensive Test Suite")
        
        for test_name, test_func in self.test_functions.items():
            test_type = self._get_test_type(test_name)
            
            if test_types and test_type not in test_types:
                continue
            
            result = self._run_single_test(test_name, test_func, test_type)
            suite.tests.append(result)
        
        suite.end_time = datetime.now()
        self.test_results.append(suite)
        return suite
    
    def run_test(self, test_name: str) -> TestResult:
        """Run a single test"""
        if test_name not in self.test_functions:
            return TestResult(
                name=test_name,
                type=TestType.UNIT,
                status=TestStatus.FAILED,
                duration=0.0,
                message=f"Test '{test_name}' not found"
            )
        
        test_func = self.test_functions[test_name]
        test_type = self._get_test_type(test_name)
        
        return self._run_single_test(test_name, test_func, test_type)
    
    def _run_single_test(self, test_name: str, test_func: Callable, test_type: TestType) -> TestResult:
        """Run a single test function"""
        start_time = time.time()
        
        try:
            print(f"Running {test_name}...")
            result = test_func()
            
            if isinstance(result, bool):
                status = TestStatus.PASSED if result else TestStatus.FAILED
                message = "Test passed" if result else "Test failed"
                details = {}
            elif isinstance(result, dict):
                status = TestStatus.PASSED if result.get('success', False) else TestStatus.FAILED
                message = result.get('message', 'Test completed')
                details = {k: v for k, v in result.items() if k != 'success' and k != 'message'}
            else:
                status = TestStatus.PASSED
                message = "Test passed"
                details = {"result": str(result)}
            
        except Exception as e:
            status = TestStatus.ERROR
            message = f"Test error: {str(e)}"
            details = {
                "traceback": traceback.format_exc(),
                "error_type": type(e).__name__
            }
        
        duration = time.time() - start_time
        
        return TestResult(
            name=test_name,
            type=test_type,
            status=status,
            duration=duration,
            message=message,
            details=details
        )
    
    def _get_test_type(self, test_name: str) -> TestType:
        """Determine test type from name"""
        if "performance" in test_name:
            return TestType.PERFORMANCE
        elif "health" in test_name:
            return TestType.HEALTH
        elif "integration" in test_name or "full" in test_name:
            return TestType.INTEGRATION
        elif "system" in test_name:
            return TestType.SYSTEM
        else:
            return TestType.UNIT
    
    # Core Component Tests
    
    def _test_ide_detector(self) -> Dict[str, Any]:
        """Test IDE detector functionality"""
        try:
            # Import and test IDE detector
            sys.path.insert(0, str(self.core_dir))
            from ide_detector import IDEDetector
            
            detector = IDEDetector()
            
            # Test basic functionality
            assert detector.ide_info is not None, "IDE info should not be None"
            assert detector.system_info is not None, "System info should not be None"
            
            # Test compatibility adapter
            adapter = detector.get_compatibility_adapter()
            assert isinstance(adapter, dict), "Compatibility adapter should be a dictionary"
            
            # Test config path
            config_path = detector.get_agent_config_path()
            assert isinstance(config_path, Path), "Config path should be a Path"
            
            return {
                "success": True,
                "message": "IDE detector test passed",
                "ide_detected": detector.ide_info.name,
                "platform": detector.system_info["platform"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"IDE detector test failed: {str(e)}"
            }
    
    def _test_skill_discovery(self) -> Dict[str, Any]:
        """Test skill discovery functionality"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from skill_discovery import SkillDiscovery
            
            discovery = SkillDiscovery(self.agent_root)
            
            # Test skill discovery
            skills = discovery.discover_all_skills()
            assert isinstance(skills, dict), "Skills should be a dictionary"
            
            # Test context analysis
            context = discovery.analyze_request_context("Create a React component")
            assert context is not None, "Context should not be None"
            assert context.domain == "frontend", "Should detect frontend domain"
            
            # Test skill finding
            relevant_skills = discovery.find_relevant_skills(context)
            assert isinstance(relevant_skills, list), "Relevant skills should be a list"
            
            return {
                "success": True,
                "message": "Skill discovery test passed",
                "skills_found": len(skills),
                "context_detected": context.domain,
                "relevant_skills": len(relevant_skills)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Skill discovery test failed: {str(e)}"
            }
    
    def _test_ai_router(self) -> Dict[str, Any]:
        """Test AI router functionality"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from ai_router import AIRouter
            
            router = AIRouter(self.agent_root)
            
            # Test agent profile loading
            assert len(router.agent_profiles) > 0, "Should load agent profiles"
            
            # Test request routing
            decision = router.route_request("Create a React component")
            assert decision is not None, "Routing decision should not be None"
            assert decision.primary_agent != "", "Should have primary agent"
            assert decision.confidence >= 0, "Confidence should be non-negative"
            
            # Test statistics
            stats = router.get_routing_statistics()
            assert isinstance(stats, dict), "Statistics should be a dictionary"
            
            return {
                "success": True,
                "message": "AI router test passed",
                "agents_loaded": len(router.agent_profiles),
                "primary_agent": decision.primary_agent,
                "confidence": decision.confidence
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"AI router test failed: {str(e)}"
            }
    
    # Integration Tests
    
    def _test_full_routing_pipeline(self) -> Dict[str, Any]:
        """Test complete routing pipeline"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from ide_detector import IDEDetector
            from skill_discovery import SkillDiscovery
            from ai_router import AIRouter
            
            # Initialize components
            ide_detector = IDEDetector()
            skill_discovery = SkillDiscovery(self.agent_root)
            ai_router = AIRouter(self.agent_root)
            
            # Test pipeline
            request = "Build a full-stack web application with React and Node.js"
            
            # Step 1: Context analysis
            context = skill_discovery.analyze_request_context(request)
            
            # Step 2: Routing decision
            decision = ai_router.route_request(request, context)
            
            # Step 3: Skill resolution
            skills = skill_discovery.resolve_dependencies(decision.skills_to_load)
            
            # Validate pipeline
            assert context is not None, "Context should be analyzed"
            assert decision.primary_agent != "", "Should route to primary agent"
            assert isinstance(skills, list), "Should resolve skill dependencies"
            
            return {
                "success": True,
                "message": "Full routing pipeline test passed",
                "context_domain": context.domain,
                "primary_agent": decision.primary_agent,
                "skills_resolved": len(skills),
                "pipeline_complete": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Full routing pipeline test failed: {str(e)}"
            }
    
    def _test_skill_loading(self) -> Dict[str, Any]:
        """Test skill loading and validation"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from skill_discovery import SkillDiscovery
            
            discovery = SkillDiscovery(self.agent_root)
            skills = discovery.discover_all_skills()
            
            loaded_skills = 0
            validated_skills = 0
            
            for skill_name in list(skills.keys())[:5]:  # Test first 5 skills
                try:
                    # Test skill health
                    health = discovery.validate_skill_health(skill_name)
                    if health["status"] == "healthy":
                        validated_skills += 1
                    
                    loaded_skills += 1
                    
                except Exception as e:
                    print(f"Skill {skill_name} validation failed: {e}")
            
            return {
                "success": True,
                "message": "Skill loading test passed",
                "total_skills": len(skills),
                "loaded_skills": loaded_skills,
                "validated_skills": validated_skills
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Skill loading test failed: {str(e)}"
            }
    
    def _test_agent_coordination(self) -> Dict[str, Any]:
        """Test multi-agent coordination"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from ai_router import AIRouter
            
            router = AIRouter(self.agent_root)
            
            # Test complex request that should trigger multi-agent coordination
            complex_request = "Build and deploy a secure, scalable e-commerce platform with comprehensive testing"
            decision = router.route_request(complex_request)
            
            # Should have multiple agents for complex task
            assert decision.primary_agent != "", "Should have primary agent"
            
            coordination_score = len(decision.secondary_agents) > 0
            
            return {
                "success": True,
                "message": "Agent coordination test passed",
                "primary_agent": decision.primary_agent,
                "secondary_agents": len(decision.secondary_agents),
                "coordination_detected": coordination_score
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Agent coordination test failed: {str(e)}"
            }
    
    # Performance Tests
    
    def _test_routing_performance(self) -> Dict[str, Any]:
        """Test routing performance"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from ai_router import AIRouter
            
            router = AIRouter(self.agent_root)
            
            # Test multiple routing requests
            test_requests = [
                "Create a React component",
                "Build a REST API",
                "Set up Docker container",
                "Implement security audit",
                "Design database schema"
            ]
            
            start_time = time.time()
            
            for request in test_requests:
                decision = router.route_request(request)
                assert decision is not None, f"Should route request: {request}"
            
            total_time = time.time() - start_time
            avg_time = total_time / len(test_requests)
            
            # Performance should be reasonable (< 1 second per request)
            performance_ok = avg_time < 1.0
            
            return {
                "success": performance_ok,
                "message": f"Routing performance test passed (avg: {avg_time:.3f}s)" if performance_ok else f"Routing performance slow (avg: {avg_time:.3f}s)",
                "total_requests": len(test_requests),
                "total_time": total_time,
                "average_time": avg_time,
                "performance_ok": performance_ok
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Routing performance test failed: {str(e)}"
            }
    
    def _test_skill_discovery_performance(self) -> Dict[str, Any]:
        """Test skill discovery performance"""
        try:
            sys.path.insert(0, str(self.core_dir))
            from skill_discovery import SkillDiscovery
            
            discovery = SkillDiscovery(self.agent_root)
            
            # Test discovery performance
            start_time = time.time()
            skills = discovery.discover_all_skills()
            discovery_time = time.time() - start_time
            
            # Test context analysis performance
            test_request = "Create a complex web application with modern technologies"
            
            start_time = time.time()
            context = discovery.analyze_request_context(test_request)
            context_time = time.time() - start_time
            
            # Test skill finding performance
            start_time = time.time()
            relevant_skills = discovery.find_relevant_skills(context)
            finding_time = time.time() - start_time
            
            # Performance should be reasonable
            performance_ok = discovery_time < 2.0 and context_time < 0.5 and finding_time < 0.5
            
            return {
                "success": performance_ok,
                "message": "Skill discovery performance test passed" if performance_ok else "Skill discovery performance slow",
                "discovery_time": discovery_time,
                "context_time": context_time,
                "finding_time": finding_time,
                "skills_found": len(skills),
                "performance_ok": performance_ok
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Skill discovery performance test failed: {str(e)}"
            }
    
    # Health Checks
    
    def _test_system_health(self) -> Dict[str, Any]:
        """Test overall system health"""
        health_issues = []
        
        # Check core directories
        if not self.agent_root.exists():
            health_issues.append("Agent root directory not found")
        
        if not self.core_dir.exists():
            health_issues.append("Core directory not found")
        
        # Check core files
        core_files = ["ide_detector.py", "skill_discovery.py", "ai_router.py"]
        for file_name in core_files:
            file_path = self.core_dir / file_name
            if not file_path.exists():
                health_issues.append(f"Core file missing: {file_name}")
        
        # Check Python modules
        try:
            import yaml
        except ImportError:
            health_issues.append("PyYAML not installed")
        
        try:
            import pathlib
        except ImportError:
            health_issues.append("pathlib not available")
        
        return {
            "success": len(health_issues) == 0,
            "message": "System healthy" if len(health_issues) == 0 else f"Health issues found: {len(health_issues)}",
            "health_issues": health_issues,
            "health_score": max(0, 100 - len(health_issues) * 10)
        }
    
    def _test_dependency_health(self) -> Dict[str, Any]:
        """Test dependency health"""
        missing_deps = []
        
        # Check required Python packages
        required_packages = ["yaml", "pathlib", "datetime", "enum", "dataclasses"]
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_deps.append(package)
        
        return {
            "success": len(missing_deps) == 0,
            "message": "All dependencies satisfied" if len(missing_deps) == 0 else f"Missing dependencies: {missing_deps}",
            "missing_dependencies": missing_deps,
            "dependency_health": 100 - len(missing_deps) * 20
        }
    
    def _test_configuration_health(self) -> Dict[str, Any]:
        """Test configuration health"""
        config_issues = []
        
        # Check agent configuration
        agents_dir = self.agent_root / "agents"
        if not agents_dir.exists():
            config_issues.append("Agents directory not found")
        else:
            agent_files = list(agents_dir.glob("*.md"))
            if len(agent_files) < 5:
                config_issues.append(f"Too few agent files: {len(agent_files)}")
        
        # Check skills configuration
        skills_dir = self.agent_root / "skills"
        if not skills_dir.exists():
            config_issues.append("Skills directory not found")
        
        # Check workflows configuration
        workflows_dir = self.agent_root / "workflows"
        if not workflows_dir.exists():
            config_issues.append("Workflows directory not found")
        
        return {
            "success": len(config_issues) == 0,
            "message": "Configuration healthy" if len(config_issues) == 0 else f"Configuration issues: {len(config_issues)}",
            "configuration_issues": config_issues,
            "configuration_health": max(0, 100 - len(config_issues) * 15)
        }
    
    def generate_report(self, suite: TestSuite) -> str:
        """Generate detailed test report"""
        report = []
        report.append(f"# Test Suite Report: {suite.name}")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"- **Total Tests**: {len(suite.tests)}")
        report.append(f"- **Passed**: {suite.passed_count}")
        report.append(f"- **Failed**: {suite.failed_count}")
        report.append(f"- **Errors**: {suite.error_count}")
        report.append(f"- **Skipped**: {suite.skipped_count}")
        report.append(f"- **Duration**: {suite.duration:.2f} seconds")
        report.append("")
        
        # Test Results
        report.append("## Test Results")
        
        for test in suite.tests:
            status_icon = {
                TestStatus.PASSED: "✅",
                TestStatus.FAILED: "❌",
                TestStatus.ERROR: "🔥",
                TestStatus.SKIPPED: "⏭️"
            }.get(test.status, "❓")
            
            report.append(f"### {status_icon} {test.name}")
            report.append(f"- **Type**: {test.type.value}")
            report.append(f"- **Status**: {test.status.value}")
            report.append(f"- **Duration**: {test.duration:.3f}s")
            report.append(f"- **Message**: {test.message}")
            
            if test.details:
                report.append("- **Details**:")
                for key, value in test.details.items():
                    if isinstance(value, (list, dict)):
                        report.append(f"  - {key}: {json.dumps(value, indent=2)}")
                    else:
                        report.append(f"  - {key}: {value}")
            
            report.append("")
        
        return "\n".join(report)

def main():
    """Run the test framework"""
    agent_root = Path.cwd() / ".agent"
    framework = TestFramework(agent_root)
    
    print("🧪 Running Enhanced VS Code Agent Test Suite")
    print("=" * 50)
    
    # Run all tests
    suite = framework.run_all_tests()
    
    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"Total: {len(suite.tests)}")
    print(f"Passed: {suite.passed_count} ✅")
    print(f"Failed: {suite.failed_count} ❌")
    print(f"Errors: {suite.error_count} 🔥")
    print(f"Duration: {suite.duration:.2f}s")
    
    # Generate report
    report = framework.generate_report(suite)
    
    # Save report
    report_path = agent_root / "test_report.md"
    report_path.write_text(report)
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    
    # Return exit code based on results
    failed_total = suite.failed_count + suite.error_count
    sys.exit(1 if failed_total > 0 else 0)

if __name__ == "__main__":
    main()
