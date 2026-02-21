#!/usr/bin/env python3
"""
Main Orchestrator - Enhanced VS Code Agent System
==================================================

Central orchestration system that coordinates all components of the enhanced
VS Code agent system. Provides unified API and manages the complete workflow.

Features:
- Unified component coordination
- Request processing pipeline
- Performance monitoring
- Error handling and recovery
- Resource management
- Logging and analytics
"""

import os
import sys
import json
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import core components
from ide_detector import IDEDetector
from skill_discovery import SkillDiscovery, SkillContext
from ai_router import AIRouter, RoutingDecision
from config_manager import ConfigManager, ConfigScope
from mcp_integration import MCPIntegration, ServerCapability
from test_framework import TestFramework, TestType
from anti_hallucination import AntiHallucinationSystem, HallucinationRisk

class RequestStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ComponentStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class Request:
    """User request with metadata"""
    id: str
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: RequestStatus = RequestStatus.PENDING
    context: Optional[SkillContext] = None
    routing_decision: Optional[RoutingDecision] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    component_usage: Dict[str, float] = field(default_factory=dict)

@dataclass
class ComponentHealth:
    """Health status of a component"""
    name: str
    status: ComponentStatus
    last_check: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
    error_rate: float = 0.0
    uptime: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

class EnhancedOrchestrator:
    """Main orchestrator for the enhanced VS Code agent system"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.core_dir = agent_root / "core"
        
        # Initialize components
        self.ide_detector = None
        self.skill_discovery = None
        self.ai_router = None
        self.config_manager = None
        self.mcp_integration = None
        self.test_framework = None
        self.anti_hallucination = None
        
        # Request processing
        self.requests: Dict[str, Request] = {}
        self.request_queue: List[str] = []
        self.processing_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Monitoring
        self.component_health: Dict[str, ComponentHealth] = {}
        self.performance_metrics: Dict[str, Any] = {}
        self.active = False
        
        # Logging
        self.logger = self._setup_logging()
        
        # Initialize system
        self._initialize_system()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system"""
        logger = logging.getLogger("enhanced_orchestrator")
        logger.setLevel(logging.INFO)
        
        # Create logs directory
        logs_dir = self.agent_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(logs_dir / "orchestrator.log")
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_system(self):
        """Initialize all system components"""
        try:
            self.logger.info("Initializing Enhanced VS Code Agent System...")
            
            # Initialize IDE detector
            self.ide_detector = IDEDetector()
            self.logger.info(f"IDE detected: {self.ide_detector.ide_info.name}")
            
            # Initialize configuration manager
            self.config_manager = ConfigManager(self.agent_root)
            self.logger.info("Configuration manager initialized")
            
            # Initialize skill discovery
            self.skill_discovery = SkillDiscovery(self.agent_root)
            skills = self.skill_discovery.discover_all_skills()
            self.logger.info(f"Discovered {len(skills)} skills")
            
            # Initialize AI router
            self.ai_router = AIRouter(self.agent_root)
            self.logger.info(f"AI router initialized with {len(self.ai_router.agent_profiles)} agents")
            
            # Initialize MCP integration
            self.mcp_integration = MCPIntegration(self.agent_root)
            self.logger.info("MCP integration initialized")
            
            # Initialize test framework
            self.test_framework = TestFramework(self.agent_root)
            self.logger.info("Test framework initialized")
            
            # Initialize anti-hallucination system
            self.anti_hallucination = AntiHallucinationSystem(self.agent_root)
            self.logger.info("Anti-hallucination system initialized")
            
            # Initialize component health tracking
            self._initialize_component_health()
            
            # Optimize configuration
            optimization = self.config_manager.optimize_configuration()
            self.logger.info(f"Configuration optimized: {len(optimization['optimizations'])} optimizations applied")
            
            # Start monitoring
            self._start_monitoring()
            
            # Perform initial health check
            self._check_component_health()
            
            self.active = True
            self.logger.info("System initialization completed successfully")
            
        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            self.logger.error(traceback.format_exc())
            raise
    
    def _initialize_component_health(self):
        """Initialize component health tracking"""
        components = [
            "ide_detector",
            "skill_discovery", 
            "ai_router",
            "config_manager",
            "mcp_integration",
            "test_framework"
        ]
        
        for component in components:
            self.component_health[component] = ComponentHealth(
                name=component,
                status=ComponentStatus.UNKNOWN
            )
    
    def _start_monitoring(self):
        """Start system monitoring"""
        def monitor():
            while self.active:
                try:
                    self._check_component_health()
                    self._update_performance_metrics()
                    time.sleep(60)  # Monitor every minute
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                    time.sleep(30)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def _check_component_health(self):
        """Check health of all components"""
        for component_name, health in self.component_health.items():
            try:
                start_time = time.time()
                
                if component_name == "ide_detector":
                    # Test IDE detector
                    ide_info = self.ide_detector.ide_info
                    if ide_info:
                        health.status = ComponentStatus.HEALTHY
                    else:
                        health.status = ComponentStatus.ERROR
                
                elif component_name == "skill_discovery":
                    # Test skill discovery
                    skills_count = len(self.skill_discovery.skills_registry)
                    if skills_count > 0:
                        health.status = ComponentStatus.HEALTHY
                        health.details["skills_count"] = skills_count
                    else:
                        health.status = ComponentStatus.DEGRADED
                
                elif component_name == "ai_router":
                    # Test AI router
                    agents_count = len(self.ai_router.agent_profiles)
                    if agents_count > 0:
                        health.status = ComponentStatus.HEALTHY
                        health.details["agents_count"] = agents_count
                    else:
                        health.status = ComponentStatus.ERROR
                
                elif component_name == "config_manager":
                    # Test config manager
                    validation = self.config_manager.validate_configuration()
                    if validation["valid"]:
                        health.status = ComponentStatus.HEALTHY
                        health.details["health_score"] = validation["health_score"]
                    else:
                        health.status = ComponentStatus.DEGRADED
                
                elif component_name == "mcp_integration":
                    # Test MCP integration
                    summary = self.mcp_integration.get_integration_summary()
                    if summary["running_servers"] > 0:
                        health.status = ComponentStatus.HEALTHY
                        health.details.update(summary)
                    else:
                        health.status = ComponentStatus.DEGRADED
                
                elif component_name == "test_framework":
                    # Test framework is always healthy if initialized
                    health.status = ComponentStatus.HEALTHY
                
                # Update response time
                health.response_time = time.time() - start_time
                health.last_check = datetime.now()
                
            except Exception as e:
                health.status = ComponentStatus.ERROR
                health.details["error"] = str(e)
                self.logger.error(f"Health check failed for {component_name}: {e}")
    
    def _update_performance_metrics(self):
        """Update performance metrics"""
        try:
            # Request metrics
            total_requests = len(self.requests)
            completed_requests = len([r for r in self.requests.values() if r.status == RequestStatus.COMPLETED])
            failed_requests = len([r for r in self.requests.values() if r.status == RequestStatus.FAILED])
            
            # Average processing time
            completed_times = [r.processing_time for r in self.requests.values() if r.processing_time > 0]
            avg_processing_time = sum(completed_times) / len(completed_times) if completed_times else 0
            
            # Component usage
            component_usage = {}
            for request in self.requests.values():
                for component, usage_time in request.component_usage.items():
                    component_usage[component] = component_usage.get(component, 0) + usage_time
            
            self.performance_metrics = {
                "total_requests": total_requests,
                "completed_requests": completed_requests,
                "failed_requests": failed_requests,
                "success_rate": completed_requests / total_requests if total_requests > 0 else 0,
                "average_processing_time": avg_processing_time,
                "component_usage": component_usage,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def process_request(self, request_text: str) -> Dict[str, Any]:
        """Process a user request through the complete pipeline"""
        
        # Generate request ID
        request_id = f"req_{int(time.time() * 1000)}"
        
        # Create request object
        request = Request(id=request_id, text=request_text)
        self.requests[request_id] = request
        
        try:
            self.logger.info(f"Processing request {request_id}: {request_text[:100]}...")
            
            # Step 1: Analyze context
            start_time = time.time()
            request.context = self.skill_discovery.analyze_request_context(request_text)
            context_time = time.time() - start_time
            request.component_usage["skill_discovery"] = context_time
            
            # Step 2: Route to agents
            start_time = time.time()
            request.routing_decision = self.ai_router.route_request(request_text, request.context)
            routing_time = time.time() - start_time
            request.component_usage["ai_router"] = routing_time
            
            # Step 3: Load required skills
            start_time = time.time()
            loaded_skills = []
            for skill_name in request.routing_decision.skills_to_load:
                # Simulate skill loading (in real implementation, this would load actual skills)
                loaded_skills.append(skill_name)
            skill_loading_time = time.time() - start_time
            request.component_usage["skill_loading"] = skill_loading_time
            
            # Step 4: Execute the task
            start_time = time.time()
            result = self._execute_task(request)
            execution_time = time.time() - start_time
            request.component_usage["task_execution"] = execution_time
            
            # Step 5: Anti-hallucination validation
            start_time = time.time()
            hallucination_check = self._validate_response(result, request)
            validation_time = time.time() - start_time
            request.component_usage["hallucination_validation"] = validation_time
            
            # Step 6: Prepare response
            request.result = result
            request.status = RequestStatus.COMPLETED
            request.processing_time = sum(request.component_usage.values())
            
            self.logger.info(f"Request {request_id} completed in {request.processing_time:.2f}s")
            
            return {
                "success": True,
                "request_id": request_id,
                "result": result,
                "routing": {
                    "primary_agent": request.routing_decision.primary_agent,
                    "secondary_agents": request.routing_decision.secondary_agents,
                    "confidence": request.routing_decision.confidence,
                    "skills_loaded": loaded_skills
                },
                "performance": {
                    "total_time": request.processing_time,
                    "component_usage": request.component_usage
                }
            }
            
        except Exception as e:
            request.status = RequestStatus.FAILED
            request.error = str(e)
            request.processing_time = sum(request.component_usage.values())
            
            self.logger.error(f"Request {request_id} failed: {e}")
            self.logger.error(traceback.format_exc())
            
            return {
                "success": False,
                "request_id": request_id,
                "error": str(e),
                "performance": {
                    "total_time": request.processing_time,
                    "component_usage": request.component_usage
                }
            }
    
    def _execute_task(self, request: Request) -> Dict[str, Any]:
        """Execute the task based on routing decision"""
        routing = request.routing_decision
        
        # Simulate task execution based on agent and context
        result = {
            "task_completed": True,
            "primary_agent": routing.primary_agent,
            "execution_plan": routing.execution_plan,
            "context": {
                "domain": request.context.domain,
                "complexity": request.context.complexity,
                "technologies": list(request.context.technologies),
                "frameworks": list(request.context.frameworks)
            },
            "output": f"Task executed by {routing.primary_agent} with confidence {routing.confidence:.2f}"
        }
        
        # Add secondary agent contributions if any
        if routing.secondary_agents:
            result["secondary_contributions"] = [
                f"Input from {agent}" for agent in routing.secondary_agents
            ]
        
        return result
    
    def _validate_response(self, result: Dict[str, Any], request: Request) -> Dict[str, Any]:
        """Validate response for hallucination risks"""
        
        # Extract response text for validation
        response_text = result.get("output", "")
        
        # Create context for validation
        context = {
            "domain": request.context.domain if request.context else "general",
            "technologies": list(request.context.technologies) if request.context else [],
            "frameworks": list(request.context.frameworks) if request.context else [],
            "intent": request.context.intent if request.context else "general",
            "complexity": request.context.complexity if request.context else "moderate"
        }
        
        # Run anti-hallucination validation
        validation_result = self.anti_hallucination.analyze_response(response_text, context)
        
        # Add validation metadata to result
        result["hallucination_check"] = {
            "risk_level": validation_result.overall_risk.value,
            "confidence_score": validation_result.confidence_score,
            "warnings": validation_result.warnings,
            "recommendations": validation_result.recommendations,
            "verified_facts": validation_result.verified_facts,
            "uncertain_claims": validation_result.uncertain_claims
        }
        
        # If high risk, add warning to output
        if validation_result.overall_risk in [HallucinationRisk.HIGH, HallucinationRisk.CRITICAL]:
            warning_text = "\n\n⚠️ **Hallucination Warning**: This response contains unverified claims. Please verify before use."
            result["output"] = result.get("output", "") + warning_text
        
        return validation_result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        # Component health
        component_status = {}
        for name, health in self.component_health.items():
            component_status[name] = {
                "status": health.status.value,
                "response_time": health.response_time,
                "last_check": health.last_check.isoformat(),
                "details": health.details
            }
        
        # Performance metrics
        metrics = self.performance_metrics.copy()
        
        # System information
        system_info = {
            "ide_info": self.ide_detector.to_dict(),
            "agent_root": str(self.agent_root),
            "active": self.active,
            "uptime": time.time() if self.active else 0
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_info": system_info,
            "component_health": component_status,
            "performance_metrics": metrics,
            "configuration": {
                "validation": self.config_manager.validate_configuration(),
                "summary": self.config_manager.get_configuration_summary()
            },
            "mcp_integration": self.mcp_integration.get_integration_summary(),
            "skills": {
                "total": len(self.skill_discovery.skills_registry),
                "categories": self.skill_discovery.get_skills_summary()["categories"]
            },
            "agents": {
                "total": len(self.ai_router.agent_profiles),
                "statistics": self.ai_router.get_routing_statistics()
            }
        }
    
    def run_system_tests(self, test_types: Optional[List[TestType]] = None) -> Dict[str, Any]:
        """Run system tests"""
        try:
            self.logger.info("Running system tests...")
            
            # Run tests
            test_suite = self.test_framework.run_all_tests(test_types)
            
            # Generate report
            report = self.test_framework.generate_report(test_suite)
            
            # Save report
            report_path = self.agent_root / "system_test_report.md"
            report_path.write_text(report)
            
            results = {
                "success": test_suite.failed_count == 0 and test_suite.error_count == 0,
                "summary": {
                    "total": len(test_suite.tests),
                    "passed": test_suite.passed_count,
                    "failed": test_suite.failed_count,
                    "errors": test_suite.error_count,
                    "skipped": test_suite.skipped_count,
                    "duration": test_suite.duration
                },
                "report_path": str(report_path),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"System tests completed: {test_suite.passed_count}/{len(test_suite.tests)} passed")
            
            return results
            
        except Exception as e:
            self.logger.error(f"System tests failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def optimize_system(self) -> Dict[str, Any]:
        """Optimize system performance"""
        optimizations = []
        
        try:
            # Optimize configuration
            config_optimization = self.config_manager.optimize_configuration()
            optimizations.extend(config_optimization["optimizations"])
            
            # Optimize MCP servers
            mcp_summary = self.mcp_integration.get_integration_summary()
            if mcp_summary["average_health"] < 0.7:
                # Restart unhealthy servers
                for server_name, server in self.mcp_integration.servers.items():
                    if server.health_score < 0.5:
                        if self.mcp_integration.restart_server(server_name):
                            optimizations.append(f"Restarted unhealthy MCP server: {server_name}")
            
            # Optimize skill discovery cache
            if len(self.skill_discovery.skills_registry) > 50:
                # Clear old cache entries
                cache_size_before = len(self.skill_discovery.context_cache)
                self.skill_discovery.context_cache.clear()
                optimizations.append(f"Cleared skill discovery cache ({cache_size_before} entries)")
            
            # Optimize AI router performance
            routing_stats = self.ai_router.get_routing_statistics()
            if routing_stats.get("recent_confidence", 0) < 0.6:
                optimizations.append("AI router confidence below threshold, consider retraining")
            
            return {
                "success": True,
                "optimizations": optimizations,
                "performance_improvement": "System optimized for better performance",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"System optimization failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def shutdown(self):
        """Gracefully shutdown the system"""
        self.logger.info("Shutting down Enhanced VS Code Agent System...")
        
        self.active = False
        
        # Shutdown MCP integration
        if self.mcp_integration:
            self.mcp_integration.shutdown()
        
        # Shutdown thread pool
        self.executor.shutdown(wait=True)
        
        self.logger.info("System shutdown completed")
    
    def get_api_endpoints(self) -> Dict[str, Any]:
        """Get available API endpoints"""
        return {
            "process_request": {
                "method": "POST",
                "description": "Process a user request",
                "parameters": {
                    "request_text": "string - The user request to process"
                }
            },
            "get_system_status": {
                "method": "GET",
                "description": "Get comprehensive system status",
                "parameters": {}
            },
            "run_system_tests": {
                "method": "POST", 
                "description": "Run system tests",
                "parameters": {
                    "test_types": "array - Optional list of test types to run"
                }
            },
            "optimize_system": {
                "method": "POST",
                "description": "Optimize system performance",
                "parameters": {}
            },
            "get_configuration": {
                "method": "GET",
                "description": "Get current configuration",
                "parameters": {}
            },
            "update_configuration": {
                "method": "PUT",
                "description": "Update configuration settings",
                "parameters": {
                    "key": "string - Configuration key",
                    "value": "any - Configuration value",
                    "scope": "string - Configuration scope"
                }
            }
        }

def main():
    """Main entry point for the enhanced orchestrator"""
    agent_root = Path.cwd() / ".agent"
    
    print("🚀 Enhanced VS Code Agent System")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = EnhancedOrchestrator(agent_root)
    
    try:
        # Show system status
        status = orchestrator.get_system_status()
        print(f"✅ System initialized successfully")
        print(f"📊 IDE: {status['system_info']['ide_info']['ide']['name']}")
        print(f"🧠 Agents: {status['agents']['total']}")
        print(f"🛠️ Skills: {status['skills']['total']}")
        print(f"🔌 MCP Servers: {status['mcp_integration']['total_servers']}")
        
        # Run system tests
        print("\n🧪 Running system tests...")
        test_results = orchestrator.run_system_tests()
        if test_results["success"]:
            print(f"✅ All tests passed ({test_results['summary']['passed']}/{test_results['summary']['total']})")
        else:
            print(f"❌ Some tests failed ({test_results['summary']['failed']} failed, {test_results['summary']['errors']} errors)")
        
        # Example request processing
        print("\n💬 Processing example request...")
        example_request = "Create a React component with TypeScript and Tailwind CSS"
        result = orchestrator.process_request(example_request)
        
        if result["success"]:
            print(f"✅ Request processed successfully")
            print(f"🎯 Primary agent: {result['routing']['primary_agent']}")
            print(f"⚡ Confidence: {result['routing']['confidence']:.2f}")
            print(f"🛠️ Skills loaded: {len(result['routing']['skills_loaded'])}")
            print(f"⏱️ Processing time: {result['performance']['total_time']:.2f}s")
        else:
            print(f"❌ Request processing failed: {result['error']}")
        
        # Show available API endpoints
        print("\n🔗 Available API endpoints:")
        endpoints = orchestrator.get_api_endpoints()
        for endpoint, info in endpoints.items():
            print(f"  {info['method']} /{endpoint} - {info['description']}")
        
        print(f"\n📈 System is ready and operational!")
        print(f"📊 System status: {'Healthy' if all(h['status'] == 'healthy' for h in status['component_health'].values()) else 'Degraded'}")
        
        # Keep system running (in real implementation, this would be a web server)
        print(f"\n🔄 System monitoring active. Press Ctrl+C to shutdown.")
        
        try:
            while True:
                time.sleep(10)
                # In real implementation, this would handle incoming requests
        except KeyboardInterrupt:
            print(f"\n👋 Shutting down...")
            orchestrator.shutdown()
            
    except Exception as e:
        print(f"❌ System error: {e}")
        orchestrator.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
