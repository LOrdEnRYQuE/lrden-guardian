#!/usr/bin/env python3
"""
Enhanced MCP Server Integration - Enhanced VS Code Agent System
==============================================================

Advanced Model Context Protocol (MCP) server management with automatic
discovery, health monitoring, and intelligent server selection.

Features:
- Automatic MCP server discovery
- Health monitoring and recovery
- Intelligent server selection
- Load balancing and failover
- Server capability analysis
- Dynamic configuration
"""

import os
import json
import subprocess
import time
import socket
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
import requests

class ServerStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"
    STARTING = "starting"
    STOPPING = "stopping"

class ServerCapability(Enum):
    FILE_SYSTEM = "file_system"
    DATABASE = "database"
    WEB_SCRAPING = "web_scraping"
    AI_MODELS = "ai_models"
    SEARCH = "search"
    COMMUNICATION = "communication"
    AUTOMATION = "automation"
    MONITORING = "monitoring"

@dataclass
class MCPServer:
    """MCP Server configuration and status"""
    name: str
    command: str
    args: List[str]
    capabilities: List[ServerCapability]
    status: ServerStatus = ServerStatus.UNKNOWN
    pid: Optional[int] = None
    port: Optional[int] = None
    health_score: float = 0.0
    last_health_check: Optional[datetime] = None
    response_time: float = 0.0
    error_count: int = 0
    success_count: int = 0
    config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.capabilities, str):
            self.capabilities = [ServerCapability(c) for c in self.capabilities.split(',')]
        elif isinstance(self.capabilities, list) and self.capabilities and isinstance(self.capabilities[0], str):
            self.capabilities = [ServerCapability(c) for c in self.capabilities]

@dataclass
class ServerSelection:
    """Server selection result"""
    primary_server: str
    backup_servers: List[str]
    selection_reason: str
    confidence: float
    estimated_performance: float

class MCPIntegration:
    """Enhanced MCP server integration and management"""
    
    def __init__(self, agent_root: Path):
        self.agent_root = agent_root
        self.config_dir = agent_root / "config"
        self.mcp_config_path = self.config_dir / "mcp_config.json"
        
        self.servers: Dict[str, MCPServer] = {}
        self.server_processes: Dict[str, subprocess.Popen] = {}
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Load configuration
        self._load_mcp_config()
        
        # Start monitoring
        self._start_monitoring()
    
    def _load_mcp_config(self):
        """Load MCP server configuration"""
        
        # Default servers
        default_servers = {
            "filesystem": {
                "command": "python",
                "args": ["-m", "mcp_filesystem"],
                "capabilities": ["file_system"],
                "config": {"allowed_directories": [str(self.agent_root.parent)]}
            },
            "database": {
                "command": "python", 
                "args": ["-m", "mcp_database"],
                "capabilities": ["database"],
                "config": {"database_url": "sqlite:///agent.db"}
            },
            "web_search": {
                "command": "python",
                "args": ["-m", "mcp_websearch"],
                "capabilities": ["search", "web_scraping"],
                "config": {"api_key": "${WEB_SEARCH_API_KEY}"}
            },
            "ai_models": {
                "command": "python",
                "args": ["-m", "mcp_ai"],
                "capabilities": ["ai_models"],
                "config": {"model": "gpt-4", "api_key": "${OPENAI_API_KEY}"}
            },
            "communication": {
                "command": "python",
                "args": ["-m", "mcp_communication"],
                "capabilities": ["communication"],
                "config": {"email_provider": "smtp"}
            },
            "automation": {
                "command": "python",
                "args": ["-m", "mcp_automation"],
                "capabilities": ["automation"],
                "config": {"max_concurrent_tasks": 10}
            }
        }
        
        # Load existing configuration
        loaded_config = {}
        if self.mcp_config_path.exists():
            try:
                with open(self.mcp_config_path, 'r') as f:
                    loaded_config = json.load(f)
            except Exception as e:
                print(f"Error loading MCP config: {e}")
        
        # Merge with defaults
        mcp_servers = loaded_config.get("mcpServers", {})
        
        # Add default servers if not present
        for server_name, server_config in default_servers.items():
            if server_name not in mcp_servers:
                mcp_servers[server_name] = server_config
        
        # Create server objects
        for server_name, server_config in mcp_servers.items():
            server = MCPServer(
                name=server_name,
                command=server_config.get("command", ""),
                args=server_config.get("args", []),
                capabilities=server_config.get("capabilities", []),
                config=server_config.get("config", {})
            )
            self.servers[server_name] = server
    
    def _start_monitoring(self):
        """Start server monitoring thread"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_servers, daemon=True)
        self.monitoring_thread.start()
    
    def _monitor_servers(self):
        """Monitor server health and status"""
        while self.monitoring_active:
            try:
                for server_name, server in self.servers.items():
                    self._check_server_health(server)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in server monitoring: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_server_health(self, server: MCPServer):
        """Check health of a specific server"""
        try:
            # Check if process is running
            if server.pid and server.pid in self.server_processes:
                process = self.server_processes[server.pid]
                if process.poll() is not None:
                    # Process has terminated
                    server.status = ServerStatus.STOPPED
                    server.error_count += 1
                    del self.server_processes[server.pid]
                    server.pid = None
                else:
                    # Process is running, check responsiveness
                    if server.port:
                        response_time = self._test_server_responsiveness(server.port)
                        if response_time > 0:
                            server.response_time = response_time
                            server.status = ServerStatus.RUNNING
                            server.success_count += 1
                        else:
                            server.status = ServerStatus.ERROR
                            server.error_count += 1
            else:
                # Try to start server if needed
                if server.status == ServerStatus.STOPPED:
                    self._start_server(server)
            
            # Update health score
            server.health_score = self._calculate_health_score(server)
            server.last_health_check = datetime.now()
            
        except Exception as e:
            print(f"Error checking health for {server.name}: {e}")
            server.status = ServerStatus.ERROR
            server.error_count += 1
    
    def _start_server(self, server: MCPServer) -> bool:
        """Start an MCP server"""
        try:
            # Prepare command
            cmd = [server.command] + server.args
            
            # Set environment variables from config
            env = os.environ.copy()
            for key, value in server.config.items():
                if key.endswith("_key") or key.endswith("_token"):
                    # Handle API keys and tokens
                    if value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]
                        if env_var in os.environ:
                            env[key.upper()] = os.environ[env_var]
            
            # Start process
            process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            server.status = ServerStatus.STARTING
            server.pid = process.pid
            self.server_processes[process.pid] = process
            
            # Wait a bit for startup
            time.sleep(2)
            
            # Check if still running
            if process.poll() is None:
                server.status = ServerStatus.RUNNING
                server.success_count += 1
                return True
            else:
                server.status = ServerStatus.ERROR
                server.error_count += 1
                return False
                
        except Exception as e:
            print(f"Error starting server {server.name}: {e}")
            server.status = ServerStatus.ERROR
            server.error_count += 1
            return False
    
    def _test_server_responsiveness(self, port: int) -> float:
        """Test server responsiveness with a simple request"""
        try:
            start_time = time.time()
            
            # Try to connect to server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                return time.time() - start_time
            else:
                return -1.0
                
        except Exception:
            return -1.0
    
    def _calculate_health_score(self, server: MCPServer) -> float:
        """Calculate health score for a server"""
        if server.status == ServerStatus.RUNNING:
            base_score = 0.8
            
            # Response time factor (lower is better)
            if server.response_time > 0:
                time_factor = max(0, 1.0 - (server.response_time / 5.0))  # 5 seconds is poor
                base_score += time_factor * 0.2
            
            # Success rate factor
            total_requests = server.success_count + server.error_count
            if total_requests > 0:
                success_rate = server.success_count / total_requests
                base_score *= success_rate
            
            return min(base_score, 1.0)
        
        elif server.status == ServerStatus.STARTING:
            return 0.5
        
        elif server.status == ServerStatus.STOPPED:
            return 0.2
        
        else:  # ERROR or UNKNOWN
            return 0.0
    
    def select_server(self, required_capabilities: List[ServerCapability], max_servers: int = 3) -> ServerSelection:
        """Select best server(s) for required capabilities"""
        
        # Find servers with required capabilities
        candidate_servers = []
        
        for server_name, server in self.servers.items():
            # Check if server has required capabilities
            server_capabilities = set(server.capabilities)
            required_set = set(required_capabilities)
            
            if required_set.issubset(server_capabilities):
                # Calculate score
                score = self._calculate_server_score(server, required_capabilities)
                candidate_servers.append((server_name, score))
        
        # Sort by score
        candidate_servers.sort(key=lambda x: x[1], reverse=True)
        
        if not candidate_servers:
            # No server found with all capabilities
            return ServerSelection(
                primary_server="",
                backup_servers=[],
                selection_reason="No server found with required capabilities",
                confidence=0.0,
                estimated_performance=0.0
            )
        
        # Select primary and backup servers
        primary_server = candidate_servers[0][0]
        backup_servers = [name for name, score in candidate_servers[1:max_servers]]
        
        # Calculate confidence
        primary_score = candidate_servers[0][1]
        confidence = min(primary_score, 1.0)
        
        # Generate selection reason
        primary_server_obj = self.servers[primary_server]
        reason = f"Selected {primary_server} with capabilities {', '.join(c.value for c in primary_server_obj.capabilities)}"
        
        if backup_servers:
            reason += f" (backups: {', '.join(backup_servers)})"
        
        return ServerSelection(
            primary_server=primary_server,
            backup_servers=backup_servers,
            selection_reason=reason,
            confidence=confidence,
            estimated_performance=primary_score
        )
    
    def _calculate_server_score(self, server: MCPServer, required_capabilities: List[ServerCapability]) -> float:
        """Calculate score for server selection"""
        score = 0.0
        
        # Health score (40% weight)
        score += server.health_score * 0.4
        
        # Capability match (30% weight)
        server_capabilities = set(server.capabilities)
        required_set = set(required_capabilities)
        
        if required_set.issubset(server_capabilities):
            # Bonus for exact matches
            exact_matches = len(required_set.intersection(server_capabilities))
            capability_score = exact_matches / len(required_set)
            score += capability_score * 0.3
        
        # Response time (20% weight)
        if server.response_time > 0:
            # Lower response time = higher score
            time_score = max(0, 1.0 - (server.response_time / 2.0))  # 2 seconds is baseline
            score += time_score * 0.2
        elif server.status == ServerStatus.RUNNING:
            score += 0.1  # Running but unknown response time
        
        # Success rate (10% weight)
        total_requests = server.success_count + server.error_count
        if total_requests > 0:
            success_rate = server.success_count / total_requests
            score += success_rate * 0.1
        
        return score
    
    def start_server(self, server_name: str) -> bool:
        """Manually start a specific server"""
        if server_name not in self.servers:
            print(f"Server '{server_name}' not found")
            return False
        
        server = self.servers[server_name]
        return self._start_server(server)
    
    def stop_server(self, server_name: str) -> bool:
        """Manually stop a specific server"""
        if server_name not in self.servers:
            print(f"Server '{server_name}' not found")
            return False
        
        server = self.servers[server_name]
        
        if server.pid and server.pid in self.server_processes:
            try:
                process = self.server_processes[server.pid]
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                
                server.status = ServerStatus.STOPPED
                del self.server_processes[server.pid]
                server.pid = None
                
                return True
                
            except Exception as e:
                print(f"Error stopping server {server_name}: {e}")
                return False
        
        return True  # Already stopped
    
    def restart_server(self, server_name: str) -> bool:
        """Restart a specific server"""
        if self.stop_server(server_name):
            time.sleep(2)  # Brief pause
            return self.start_server(server_name)
        return False
    
    def get_server_status(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a specific server"""
        if server_name not in self.servers:
            return None
        
        server = self.servers[server_name]
        
        return {
            "name": server.name,
            "status": server.status.value,
            "pid": server.pid,
            "port": server.port,
            "health_score": server.health_score,
            "response_time": server.response_time,
            "success_count": server.success_count,
            "error_count": server.error_count,
            "capabilities": [c.value for c in server.capabilities],
            "last_health_check": server.last_health_check.isoformat() if server.last_health_check else None,
            "config": server.config
        }
    
    def get_all_servers_status(self) -> Dict[str, Any]:
        """Get status of all servers"""
        return {
            server_name: self.get_server_status(server_name)
            for server_name in self.servers.keys()
        }
    
    def discover_servers(self) -> List[str]:
        """Discover available MCP servers in the system"""
        discovered = []
        
        # Check common locations for MCP servers
        search_paths = [
            Path.home() / ".local" / "bin",
            Path("/usr/local/bin"),
            Path("/usr/bin"),
            self.agent_root / "servers"
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                for item in search_path.iterdir():
                    if item.is_file() and "mcp" in item.name.lower():
                        discovered.append(str(item))
        
        return discovered
    
    def add_server(self, name: str, command: str, args: List[str], capabilities: List[ServerCapability], config: Dict[str, Any] = None) -> bool:
        """Add a new MCP server"""
        if name in self.servers:
            print(f"Server '{name}' already exists")
            return False
        
        server = MCPServer(
            name=name,
            command=command,
            args=args,
            capabilities=capabilities,
            config=config or {}
        )
        
        self.servers[name] = server
        self._save_config()
        
        return True
    
    def remove_server(self, name: str) -> bool:
        """Remove an MCP server"""
        if name not in self.servers:
            print(f"Server '{name}' not found")
            return False
        
        # Stop server if running
        self.stop_server(name)
        
        # Remove from registry
        del self.servers[name]
        
        # Save updated configuration
        self._save_config()
        
        return True
    
    def _save_config(self):
        """Save current MCP configuration"""
        config = {
            "mcpServers": {}
        }
        
        for server_name, server in self.servers.items():
            config["mcpServers"][server_name] = {
                "command": server.command,
                "args": server.args,
                "capabilities": [c.value for c in server.capabilities],
                "config": server.config
            }
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Save configuration
        with open(self.mcp_config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get summary of MCP integration"""
        running_servers = sum(1 for s in self.servers.values() if s.status == ServerStatus.RUNNING)
        total_servers = len(self.servers)
        avg_health = sum(s.health_score for s in self.servers.values()) / total_servers if total_servers > 0 else 0
        
        capabilities_count = {}
        for server in self.servers.values():
            for capability in server.capabilities:
                capabilities_count[capability.value] = capabilities_count.get(capability.value, 0) + 1
        
        return {
            "total_servers": total_servers,
            "running_servers": running_servers,
            "stopped_servers": total_servers - running_servers,
            "average_health": avg_health,
            "capabilities": capabilities_count,
            "monitoring_active": self.monitoring_active,
            "config_file": str(self.mcp_config_path)
        }
    
    def shutdown(self):
        """Shutdown MCP integration"""
        # Stop monitoring
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        # Stop all servers
        for server_name in list(self.servers.keys()):
            self.stop_server(server_name)

def main():
    """Test MCP integration"""
    agent_root = Path.cwd() / ".agent"
    mcp_integration = MCPIntegration(agent_root)
    
    print("🔌 Enhanced MCP Server Integration")
    print("=" * 40)
    
    # Show integration summary
    summary = mcp_integration.get_integration_summary()
    print(f"Total servers: {summary['total_servers']}")
    print(f"Running servers: {summary['running_servers']}")
    print(f"Average health: {summary['average_health']:.2f}")
    print(f"Capabilities: {list(summary['capabilities'].keys())}")
    
    # Show server status
    print("\nServer Status:")
    all_status = mcp_integration.get_all_servers_status()
    for server_name, status in all_status.items():
        print(f"  {server_name}: {status['status']} (health: {status['health_score']:.2f})")
    
    # Test server selection
    print("\nTesting server selection:")
    selection = mcp_integration.select_server([ServerCapability.FILE_SYSTEM])
    print(f"Primary: {selection.primary_server}")
    print(f"Confidence: {selection.confidence:.2f}")
    print(f"Reason: {selection.selection_reason}")
    
    # Cleanup
    mcp_integration.shutdown()

if __name__ == "__main__":
    main()
