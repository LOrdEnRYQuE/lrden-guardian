# Enhanced VS Code Agent System

> **Universal, autonomous AI agent system for all VS Code-based IDEs**

A comprehensive, intelligent agent system that works seamlessly across VS Code, Windsurf, Cursor, and other VS Code-based IDEs. Features dynamic skill loading, AI-powered routing, and advanced automation capabilities.

---

## 🚀 Quick Start

### Installation

```bash
# Clone or copy the .agent directory to your project
cp -r .agent /path/to/your/project/

# Install dependencies
pip install pyyaml psutil requests

# Run the system
cd /path/to/your/project/.agent
python core/orchestrator.py
```

### Basic Usage

```python
from core.orchestrator import EnhancedOrchestrator
from pathlib import Path

# Initialize the system
orchestrator = EnhancedOrchestrator(Path.cwd() / ".agent")

# Process a request
result = orchestrator.process_request("Create a React component with TypeScript")
print(f"Agent: {result['routing']['primary_agent']}")
print(f"Confidence: {result['routing']['confidence']}")
```

---

## 🏗️ Architecture

### Core Components

1. **IDE Detector** (`core/ide_detector.py`)
   - Universal IDE compatibility layer
   - Automatic IDE detection (VS Code, Windsurf, Cursor, etc.)
   - Platform-specific optimizations

2. **Skill Discovery** (`core/skill_discovery.py`)
   - Dynamic skill loading and discovery
   - Context-aware skill matching
   - Dependency resolution and validation

3. **AI Router** (`core/ai_router.py`)
   - Intelligent agent selection
   - Multi-agent orchestration
   - Performance-based routing

4. **Configuration Manager** (`core/config_manager.py`)
   - Universal configuration system
   - Profile management
   - IDE-specific optimizations

5. **MCP Integration** (`core/mcp_integration.py`)
   - Advanced MCP server management
   - Health monitoring and auto-recovery
   - Load balancing and failover

6. **Test Framework** (`core/test_framework.py`)
   - Comprehensive testing suite
   - Performance benchmarking
   - Health monitoring

7. **Main Orchestrator** (`core/orchestrator.py`)
   - Central coordination system
   - Request processing pipeline
   - Performance monitoring

---

## 🎯 Key Features

### 🤖 Autonomous Operation
- **Zero Manual Selection**: AI automatically selects best agents and skills
- **Context-Aware Routing**: Intelligent routing based on request analysis
- **Dynamic Loading**: Skills loaded on-demand based on context

### 🔧 Universal Compatibility
- **Multi-IDE Support**: Works with VS Code, Windsurf, Cursor, Continue.dev, Codeium
- **Cross-Platform**: Windows, macOS, Linux support
- **Adaptive Configuration**: Automatically adapts to IDE capabilities

### ⚡ Performance Optimization
- **Intelligent Caching**: Context and skill result caching
- **Parallel Processing**: Multi-agent coordination for complex tasks
- **Resource Management**: Automatic resource optimization

### 🛡️ Reliability & Monitoring
- **Health Monitoring**: Real-time component health tracking
- **Auto-Recovery**: Automatic error detection and recovery
- **Comprehensive Testing**: Built-in test framework with continuous validation

---

## 📊 System Capabilities

### Supported Domains
- **Frontend**: React, Vue, Angular, CSS, Tailwind, UI/UX
- **Backend**: Node.js, Python, APIs, databases, authentication
- **DevOps**: Docker, Kubernetes, CI/CD, deployment
- **Mobile**: iOS, Android, React Native, Flutter
- **Security**: Vulnerability scanning, penetration testing
- **Testing**: Unit tests, E2E testing, performance testing
- **Architecture**: System design, patterns, best practices

### Agent Types (20 Available)
- `orchestrator` - Multi-agent coordination
- `frontend-specialist` - Web UI/UX development
- `backend-specialist` - API and business logic
- `database-architect` - Schema and SQL design
- `mobile-developer` - iOS/Android development
- `devops-engineer` - CI/CD and infrastructure
- `security-auditor` - Security compliance
- `test-engineer` - Testing strategies
- `performance-optimizer` - Speed and optimization
- And 11 more specialized agents...

### Skills (36 Available)
- **Frontend**: React best practices, Tailwind patterns, UI/UX design
- **Backend**: API patterns, Node.js practices, database design
- **Tools**: Docker expertise, deployment procedures
- **Quality**: Testing patterns, code review, linting
- **Security**: Vulnerability scanning, red team tactics
- And many more...

---

## 🔌 Integration

### MCP Server Integration

The system includes advanced MCP (Model Context Protocol) integration with:

```python
# Automatic server discovery and management
mcp_integration = MCPIntegration(agent_root)

# Select best server for capabilities
selection = mcp_integration.select_server([ServerCapability.FILE_SYSTEM])
print(f"Primary server: {selection.primary_server}")

# Monitor server health
status = mcp_integration.get_all_servers_status()
```

### Configuration Profiles

Create and manage configuration profiles for different environments:

```python
# Create development profile
config_manager.create_profile(
    name="development",
    scope=ConfigScope.WORKSPACE,
    settings={
        "performance": {"cache_size": 200},
        "logging": {"level": "DEBUG"}
    }
)

# Activate profile
config_manager.activate_profile("development")
```

---

## 📈 Performance Metrics

### Routing Performance
- **Average Response Time**: < 500ms for routing decisions
- **Routing Accuracy**: > 90% confidence in agent selection
- **Skill Loading**: < 2 seconds for complex skill chains

### System Health
- **Component Monitoring**: Real-time health checks every 30 seconds
- **Auto-Recovery**: Automatic restart of failed components
- **Performance Optimization**: Dynamic resource allocation

### Testing Coverage
- **Unit Tests**: Component-level validation
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Benchmarking and optimization validation

---

## 🛠️ Configuration

### Basic Configuration

```json
{
  "ide_detection": {
    "auto_detect": true,
    "fallback_agent": "orchestrator"
  },
  "skill_discovery": {
    "auto_discover": true,
    "cache_results": true,
    "validate_skills": true
  },
  "ai_routing": {
    "auto_route": true,
    "confidence_threshold": 0.7,
    "max_secondary_agents": 3
  },
  "performance": {
    "cache_size": 100,
    "parallel_processing": true,
    "optimize_for_speed": true
  }
}
```

### IDE-Specific Settings

The system automatically detects and configures for:

- **Windsurf**: AI acceleration, cascading workflows
- **VS Code**: Extension compatibility, standard APIs
- **Cursor**: AI-enhanced operations, integrated workflows
- **Continue.dev**: Custom model support, flexible configuration

---

## 🧪 Testing

### Run All Tests

```bash
cd .agent
python core/test_framework.py
```

### Run Specific Test Types

```python
# Run only performance tests
results = test_framework.run_all_tests([TestType.PERFORMANCE])

# Run health checks only
results = test_framework.run_all_tests([TestType.HEALTH])
```

### Test Categories

- **Unit Tests**: Individual component validation
- **Integration Tests**: Multi-component workflow testing
- **Performance Tests**: Speed and resource usage validation
- **Health Checks**: System health and dependency validation

---

## 📚 API Reference

### Core Methods

```python
# Process a user request
result = orchestrator.process_request("Create a web application")

# Get system status
status = orchestrator.get_system_status()

# Run system tests
tests = orchestrator.run_system_tests()

# Optimize system performance
optimization = orchestrator.optimize_system()
```

### Response Format

```json
{
  "success": true,
  "request_id": "req_1234567890",
  "result": {
    "task_completed": true,
    "primary_agent": "frontend-specialist",
    "execution_plan": [...]
  },
  "routing": {
    "primary_agent": "frontend-specialist",
    "secondary_agents": ["test-engineer"],
    "confidence": 0.85,
    "skills_loaded": ["react-best-practices", "tailwind-patterns"]
  },
  "performance": {
    "total_time": 2.34,
    "component_usage": {
      "skill_discovery": 0.12,
      "ai_router": 0.08,
      "task_execution": 2.14
    }
  }
}
```

---

## 🔧 Development

### Adding New Skills

1. Create skill directory:
```bash
mkdir .agent/skills/my-skill
```

2. Create SKILL.md:
```markdown
---
name: my-skill
description: Description of my skill
dependencies: [other-skill]
tags: [frontend, react]
---

# My Skill

Detailed instructions for the skill...
```

3. Add supporting files:
```bash
# Optional: scripts, references, assets
touch .agent/skills/my-skill/scripts/helper.py
touch .agent/skills/my-skill/references/template.md
```

### Adding New Agents

1. Create agent file:
```bash
touch .agent/agents/my-agent.md
```

2. Define agent configuration:
```markdown
---
name: my-agent
description: Specialized agent for specific domain
skills: [skill1, skill2]
priority: 5
---

# My Agent

Agent description and capabilities...
```

### Extending MCP Integration

Add new MCP servers in the configuration:

```python
mcp_integration.add_server(
    name="my-server",
    command="python",
    args=["-m", "my_mcp_server"],
    capabilities=[ServerCapability.DATABASE],
    config={"connection_string": "postgresql://..."}
)
```

---

## 🚨 Troubleshooting

### Common Issues

1. **IDE Detection Failed**
   - Check if IDE is running
   - Verify environment variables
   - Run `python core/ide_detector.py` for diagnostics

2. **Skill Discovery Not Working**
   - Verify skills directory exists
   - Check SKILL.md file format
   - Run `python core/skill_discovery.py` for testing

3. **AI Router Confidence Low**
   - Check agent profiles are loaded
   - Verify skill descriptions are detailed
   - Run system tests for validation

4. **MCP Servers Not Starting**
   - Check required dependencies
   - Verify API keys in environment
   - Review server configuration

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("enhanced_orchestrator").setLevel(logging.DEBUG)
```

### Health Check

Run comprehensive health check:

```bash
python core/orchestrator.py --check-health
```

---

## 📄 License

This project is part of the Enhanced VS Code Agent System. See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

---

## 📞 Support

For issues and questions:

- Check the troubleshooting section
- Run system tests for diagnostics
- Review logs in `.agent/logs/`
- Create GitHub issue with detailed information

---

**Built with ❤️ for the VS Code developer community**
