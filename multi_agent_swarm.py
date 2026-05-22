"""
Phase 6: Transcendence - Multi-Agent Swarms
Implements Kimi K2.5 style multi-agent swarms for collective intelligence
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import time
import json
from enum import Enum
from dataclasses import dataclass

class AgentRole(Enum):
    """Roles for agents in the swarm."""
    WORKER = "worker"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    LEARNER = "learner"

@dataclass
class Agent:
    """Individual agent in the swarm."""
    id: str
    role: AgentRole
    capabilities: List[str]
    knowledge: Dict
    performance: float = 0.5
    connections: List[str] = None
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []

class MultiAgentSwarm:
    """
    Multi-agent swarm system inspired by Kimi K2.5 architecture.
    Implements collective intelligence through agent collaboration.
    """
    
    def __init__(self, num_agents: int = 50):
        self.num_agents = num_agents
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[Dict] = []
        self.completed_tasks: List[Dict] = []
        self.knowledge_base: Dict = {}
        self.performance_history: List[float] = []
        
        # Initialize swarm
        self._initialize_swarm()
    
    def _initialize_swarm(self):
        """Initialize agents with different roles and capabilities."""
        # Role distribution
        role_distribution = {
            AgentRole.WORKER: 0.6,      # 60% workers
            AgentRole.SPECIALIST: 0.25, # 25% specialists
            AgentRole.COORDINATOR: 0.1,  # 10% coordinators
            AgentRole.LEARNER: 0.05     # 5% learners
        }
        
        # Capabilities by role
        capabilities_by_role = {
            AgentRole.WORKER: ["execute", "collect", "process"],
            AgentRole.SPECIALIST: ["analyze", "optimize", "create"],
            AgentRole.COORDINATOR: ["coordinate", "allocate", "monitor"],
            AgentRole.LEARNER: ["learn", "adapt", "improve"]
        }
        
        # Create agents
        for i in range(self.num_agents):
            # Determine role based on distribution
            rand = np.random.random()
            if rand < role_distribution[AgentRole.WORKER]:
                role = AgentRole.WORKER
            elif rand < role_distribution[AgentRole.WORKER] + role_distribution[AgentRole.SPECIALIST]:
                role = AgentRole.SPECIALIST
            elif rand < role_distribution[AgentRole.WORKER] + role_distribution[AgentRole.SPECIALIST] + role_distribution[AgentRole.COORDINATOR]:
                role = AgentRole.COORDINATOR
            else:
                role = AgentRole.LEARNER
            
            # Create agent
            agent = Agent(
                id=f"agent_{i}",
                role=role,
                capabilities=capabilities_by_role[role],
                knowledge={},
                performance=np.random.uniform(0.3, 0.7)
            )
            
            self.agents[agent.id] = agent
        
        # Create initial connections (small-world network)
        self._create_connections()
    
    def _create_connections(self):
        """Create connections between agents (small-world network)."""
        agent_ids = list(self.agents.keys())
        
        for agent_id in agent_ids:
            agent = self.agents[agent_id]
            
            # Connect to 3-5 random agents
            num_connections = np.random.randint(3, 6)
            for _ in range(num_connections):
                other_id = np.random.choice(agent_ids)
                if other_id != agent_id and other_id not in agent.connections:
                    agent.connections.append(other_id)
    
    def add_task(self, task: Dict):
        """Add a task to the queue."""
        task["id"] = f"task_{len(self.task_queue) + len(self.completed_tasks)}"
        task["status"] = "pending"
        task["assigned_to"] = None
        task["start_time"] = None
        task["end_time"] = None
        task["result"] = None
        
        self.task_queue.append(task)
    
    def allocate_tasks(self):
        """Allocate tasks to appropriate agents based on capabilities."""
        for task in self.task_queue:
            if task["status"] == "pending":
                # Find agents with required capabilities
                required_capability = task.get("capability", "execute")
                
                suitable_agents = [
                    agent for agent in self.agents.values()
                    if required_capability in agent.capabilities
                ]
                
                if suitable_agents:
                    # Select best performing agent
                    best_agent = max(suitable_agents, key=lambda a: a.performance)
                    
                    # Assign task
                    task["assigned_to"] = best_agent.id
                    task["status"] = "assigned"
                    task["start_time"] = time.time()
    
    def execute_tasks(self):
        """Execute assigned tasks."""
        for task in self.task_queue:
            if task["status"] == "assigned":
                agent = self.agents[task["assigned_to"]]
                
                # Simulate task execution
                execution_time = np.random.uniform(0.1, 0.5)
                time.sleep(0.01)  # Simulate processing
                
                # Determine success based on agent performance
                success_probability = agent.performance
                success = np.random.random() < success_probability
                
                # Update task
                task["status"] = "completed"
                task["end_time"] = time.time()
                task["result"] = "success" if success else "failure"
                
                # Update agent performance
                if success:
                    agent.performance = min(1.0, agent.performance + 0.05)
                    # Share knowledge
                    self._share_knowledge(agent, task)
                else:
                    agent.performance = max(0.1, agent.performance - 0.02)
                
                # Move to completed
                self.task_queue.remove(task)
                self.completed_tasks.append(task)
    
    def _share_knowledge(self, agent: Agent, task: Dict):
        """Share knowledge from completed task through network."""
        # Create knowledge entry
        knowledge = {
            "task": task.get("description", "unknown"),
            "result": task["result"],
            "timestamp": time.time(),
            "agent_id": agent.id
        }
        
        # Add to agent's knowledge
        agent.knowledge[task["id"]] = knowledge
        
        # Propagate to connected agents
        for connected_id in agent.connections:
            if connected_id in self.agents:
                connected_agent = self.agents[connected_id]
                connected_agent.knowledge[task["id"]] = knowledge.copy()
    
    def coordinate_agents(self):
        """Coordinate agents for collaborative tasks."""
        coordinators = [
            agent for agent in self.agents.values()
            if agent.role == AgentRole.COORDINATOR
        ]
        
        for coordinator in coordinators:
            # Monitor swarm performance
            avg_performance = np.mean([a.performance for a in self.agents.values()])
            
            # If performance is low, reorganize
            if avg_performance < 0.4:
                # Reassign connections
                self._reorganize_network()
                
                # Update coordinator knowledge
                coordinator.knowledge["reorganization"] = {
                    "timestamp": time.time(),
                    "reason": "low_performance",
                    "avg_performance": avg_performance
                }
    
    def _reorganize_network(self):
        """Reorganize agent connections for better performance."""
        # Find low-performing agents
        low_performers = [
            agent for agent in self.agents.values()
            if agent.performance < 0.3
        ]
        
        # Reconnect low performers to high performers
        high_performers = [
            agent for agent in self.agents.values()
            if agent.performance > 0.7
        ]
        
        for low_agent in low_performers:
            # Clear connections
            low_agent.connections = []
            
            # Connect to high performers
            num_connections = min(3, len(high_performers))
            for i in range(num_connections):
                low_agent.connections.append(high_performers[i].id)
    
    def learn_and_adapt(self):
        """Learn from completed tasks and adapt swarm behavior."""
        learners = [
            agent for agent in self.agents.values()
            if agent.role == AgentRole.LEARNER
        ]
        
        for learner in learners:
            # Analyze completed tasks
            successful_tasks = [
                task for task in self.completed_tasks
                if task["result"] == "success"
            ]
            
            if successful_tasks:
                # Calculate success patterns
                success_rate = len(successful_tasks) / len(self.completed_tasks)
                
                # Update knowledge base
                self.knowledge_base["success_rate"] = success_rate
                self.knowledge_base["total_tasks"] = len(self.completed_tasks)
                
                # Adapt agent capabilities based on patterns
                if success_rate < 0.6:
                    # Suggest capability improvements
                    learner.knowledge["improvement_suggestion"] = {
                        "timestamp": time.time(),
                        "suggestion": "increase_specialization"
                    }
    
    def get_swarm_status(self) -> Dict:
        """Get current swarm status."""
        avg_performance = np.mean([a.performance for a in self.agents.values()])
        
        role_counts = {}
        for agent in self.agents.values():
            role = agent.role.value
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            "total_agents": len(self.agents),
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "average_performance": avg_performance,
            "role_distribution": role_counts,
            "knowledge_base_size": len(self.knowledge_base)
        }

# Test the multi-agent swarm
if __name__ == "__main__":
    print("Digital Organism - Phase 6: Transcendence")
    print("=" * 60)
    print("Multi-Agent Swarms (Kimi K2.5 Style)\n")
    
    # Initialize swarm
    print("Initializing multi-agent swarm...")
    swarm = MultiAgentSwarm(num_agents=50)
    print(f"Created {len(swarm.agents)} agents")
    
    # Show initial status
    print("\nInitial Swarm Status:")
    status = swarm.get_swarm_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Add tasks
    print("\nAdding tasks to swarm...")
    for i in range(20):
        task = {
            "description": f"Task {i}",
            "capability": np.random.choice(["execute", "analyze", "coordinate", "learn"]),
            "priority": np.random.choice(["low", "medium", "high"])
        }
        swarm.add_task(task)
    
    print(f"Added 20 tasks")
    
    # Run swarm simulation
    print("\nRunning swarm simulation for 5 iterations...")
    for iteration in range(5):
        print(f"\nIteration {iteration + 1}:")
        
        # Allocate tasks
        swarm.allocate_tasks()
        
        # Execute tasks
        swarm.execute_tasks()
        
        # Coordinate agents
        swarm.coordinate_agents()
        
        # Learn and adapt
        swarm.learn_and_adapt()
        
        # Show status
        status = swarm.get_swarm_status()
        print(f"  Pending tasks: {status['pending_tasks']}")
        print(f"  Completed tasks: {status['completed_tasks']}")
        print(f"  Average performance: {status['average_performance']:.2f}")
        
        # Add more tasks if needed
        if status["pending_tasks"] < 5:
            for i in range(5):
                task = {
                    "description": f"Task {len(swarm.task_queue) + len(swarm.completed_tasks)}",
                    "capability": np.random.choice(["execute", "analyze", "coordinate", "learn"]),
                    "priority": np.random.choice(["low", "medium", "high"])
                }
                swarm.add_task(task)
    
    # Final status
    print("\n" + "=" * 60)
    print("Final Swarm Status")
    print("=" * 60)
    status = swarm.get_swarm_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show role distribution
    print("\nRole Distribution:")
    for role, count in status["role_distribution"].items():
        print(f"  {role}: {count}")
    
    print("\n" + "=" * 60)
    print("Phase 6 Summary")
    print("=" * 60)
    print("\n[OK] Multi-Agent Swarms: Implemented with 50 agents")
    print("[OK] Agent Roles: Worker, Specialist, Coordinator, Learner")
    print("[OK] Task Allocation: Capability-based assignment")
    print("[OK] Knowledge Sharing: Network propagation")
    print("[OK] Coordination: Performance-based reorganization")
    print("[--] Economic Metabolism: Pending (wawa)")
    print("[--] Tribe Model: Pending")
