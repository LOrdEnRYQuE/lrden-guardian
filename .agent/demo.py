#!/usr/bin/env python3
"""
Enhanced VS Code Agent System Demo
==================================

Demonstration script showing the key capabilities of the enhanced VS Code agent system.
"""

import sys
import json
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

def main():
    """Run the demonstration"""
    print("🚀 Enhanced VS Code Agent System Demo")
    print("=" * 50)
    
    try:
        # Import and initialize the orchestrator
        from orchestrator import EnhancedOrchestrator
        
        agent_root = Path(__file__).parent
        orchestrator = EnhancedOrchestrator(agent_root)
        
        print("✅ System initialized successfully!")
        
        # Show system status
        print("\n📊 System Status:")
        status = orchestrator.get_system_status()
        
        print(f"  IDE: {status['system_info']['ide_info']['ide']['name']}")
        print(f"  Platform: {status['system_info']['ide_info']['system']['platform']}")
        print(f"  Agents: {status['agents']['total']}")
        print(f"  Skills: {status['skills']['total']}")
        print(f"  MCP Servers: {status['mcp_integration']['total_servers']}")
        
        # Component health
        print("\n🏥 Component Health:")
        for component, health in status['component_health'].items():
            status_icon = "✅" if health['status'] == 'healthy' else "⚠️"
            print(f"  {status_icon} {component}: {health['status']}")
        
        # Test requests
        print("\n💬 Processing Sample Requests:")
        
        test_requests = [
            "Create a React component with TypeScript and Tailwind CSS",
            "Build a REST API with Node.js and Express",
            "Set up Docker containerization for a web application",
            "Implement comprehensive security audit for existing codebase",
            "Design a scalable microservices architecture"
        ]
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n  {i}. {request}")
            result = orchestrator.process_request(request)
            
            if result['success']:
                print(f"     ✅ Success!")
                print(f"     🎯 Primary Agent: {result['routing']['primary_agent']}")
                print(f"     ⚡ Confidence: {result['routing']['confidence']:.2f}")
                print(f"     🛠️ Skills Loaded: {len(result['routing']['skills_loaded'])}")
                print(f"     ⏱️ Processing Time: {result['performance']['total_time']:.2f}s")
                
                if result['routing']['secondary_agents']:
                    print(f"     🤝 Secondary Agents: {', '.join(result['routing']['secondary_agents'])}")
            else:
                print(f"     ❌ Failed: {result['error']}")
        
        # Performance metrics
        print("\n📈 Performance Metrics:")
        metrics = status['performance_metrics']
        if metrics:
            print(f"  Total Requests: {metrics.get('total_requests', 0)}")
            print(f"  Success Rate: {metrics.get('success_rate', 0):.1%}")
            print(f"  Average Processing Time: {metrics.get('average_processing_time', 0):.2f}s")
        
        # System capabilities
        print("\n🎯 System Capabilities:")
        
        # Agent domains
        agent_domains = set()
        for agent_name, agent in orchestrator.ai_router.agent_profiles.items():
            for domain in agent.domains:
                agent_domains.add(domain.value)
        
        print(f"  🤖 Agent Domains: {', '.join(sorted(agent_domains))}")
        
        # Skill categories
        skills_summary = orchestrator.skill_discovery.get_skills_summary()
        print(f"  🛠️ Skill Categories: {', '.join(sorted(skills_summary['categories'].keys()))}")
        
        # MCP capabilities
        mcp_summary = status['mcp_integration']
        print(f"  🔌 MCP Capabilities: {', '.join(mcp_summary['capabilities'].keys())}")
        
        # Run system tests
        print("\n🧪 Running System Tests:")
        test_results = orchestrator.run_system_tests()
        
        if test_results['success']:
            print(f"  ✅ All tests passed!")
            summary = test_results['summary']
            print(f"  📊 {summary['passed']}/{summary['total']} tests passed")
            print(f"  ⏱️ Duration: {summary['duration']:.2f}s")
        else:
            print(f"  ⚠️ Some tests failed")
            summary = test_results['summary']
            print(f"  📊 {summary['passed']}/{summary['total']} tests passed")
            print(f"  ❌ Failed: {summary['failed']}, Errors: {summary['errors']}")
        
        # Optimization
        print("\n⚡ System Optimization:")
        optimization = orchestrator.optimize_system()
        
        if optimization['success']:
            print(f"  ✅ Optimization completed")
            print(f"  🔧 Optimizations: {len(optimization['optimizations'])}")
            for opt in optimization['optimizations']:
                print(f"    - {opt}")
        else:
            print(f"  ⚠️ Optimization failed: {optimization.get('error', 'Unknown error')}")
        
        # Configuration summary
        print("\n⚙️ Configuration Summary:")
        config_summary = orchestrator.config_manager.get_configuration_summary()
        print(f"  📁 Configuration Files: {len(config_summary['configuration_files'])}")
        print(f"  👤 Profiles: {len(config_summary['profiles'])}")
        
        validation = orchestrator.config_manager.validate_configuration()
        print(f"  ✅ Configuration Valid: {validation['valid']}")
        print(f"  🏥 Health Score: {validation['health_score']}/100")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Start the full system: python .agent/core/orchestrator.py")
        print("2. Use the API endpoints for integration")
        print("3. Add custom skills and agents for your specific needs")
        print("4. Configure MCP servers for external integrations")
        print("5. Monitor system performance through the dashboard")
        
        # Shutdown
        orchestrator.shutdown()
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
