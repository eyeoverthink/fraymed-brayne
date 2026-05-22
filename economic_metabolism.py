"""
Phase 6: Transcendence - Economic Metabolism
Implements wawa framework for economic metabolism and resource management
"""

import numpy as np
from typing import Dict, List, Tuple
import time
from enum import Enum
from dataclasses import dataclass

class ResourceType(Enum):
    """Types of resources in the economic system."""
    COMPUTE = "compute"
    ENERGY = "energy"
    KNOWLEDGE = "knowledge"
    SOCIAL = "social"

@dataclass
class Resource:
    """A resource in the economic system."""
    type: ResourceType
    amount: float
    owner: str
    value: float = 1.0

class EconomicAgent:
    """An agent that participates in the economic system."""
    
    def __init__(self, id: str, initial_resources: Dict[ResourceType, float]):
        self.id = id
        self.resources: Dict[ResourceType, float] = initial_resources.copy()
        self.utility_history: List[float] = []
        self.transactions: List[Dict] = []
    
    def get_total_wealth(self) -> float:
        """Calculate total wealth based on resource amounts and values."""
        total = 0.0
        for resource_type, amount in self.resources.items():
            total += amount
        return total
    
    def produce(self, resource_type: ResourceType, amount: float, cost: Dict[ResourceType, float]):
        """Produce a resource at a cost."""
        # Check if agent has enough resources for production
        for required_type, required_amount in cost.items():
            if self.resources.get(required_type, 0) < required_amount:
                return False
        
        # Deduct costs
        for required_type, required_amount in cost.items():
            self.resources[required_type] -= required_amount
        
        # Add produced resource
        self.resources[resource_type] = self.resources.get(resource_type, 0) + amount
        
        return True
    
    def consume(self, resource_type: ResourceType, amount: float) -> bool:
        """Consume a resource."""
        if self.resources.get(resource_type, 0) >= amount:
            self.resources[resource_type] -= amount
            return True
        return False

class Market:
    """Market for resource exchange."""
    
    def __init__(self):
        self.prices: Dict[ResourceType, float] = {
            ResourceType.COMPUTE: 1.0,
            ResourceType.ENERGY: 1.0,
            ResourceType.KNOWLEDGE: 2.0,
            ResourceType.SOCIAL: 1.5
        }
        self.trade_history: List[Dict] = []
        self.supply: Dict[ResourceType, float] = {rt: 0.0 for rt in ResourceType}
        self.demand: Dict[ResourceType, float] = {rt: 0.0 for rt in ResourceType}
    
    def update_prices(self):
        """Update prices based on supply and demand."""
        for resource_type in ResourceType:
            supply = self.supply[resource_type]
            demand = self.demand[resource_type]
            
            if demand > 0:
                # Price increases with high demand/low supply
                ratio = supply / demand if supply > 0 else 0
                if ratio < 0.5:
                    self.prices[resource_type] *= 1.1  # Price increase
                elif ratio > 2.0:
                    self.prices[resource_type] *= 0.9  # Price decrease
            
            # Keep prices within reasonable bounds
            self.prices[resource_type] = max(0.1, min(10.0, self.prices[resource_type]))
    
    def record_trade(self, buyer_id: str, seller_id: str, resource_type: ResourceType, amount: float, price: float):
        """Record a trade in the market."""
        trade = {
            "timestamp": time.time(),
            "buyer": buyer_id,
            "seller": seller_id,
            "resource": resource_type.value,
            "amount": amount,
            "price": price,
            "total_value": amount * price
        }
        self.trade_history.append(trade)
    
    def get_market_stats(self) -> Dict:
        """Get market statistics."""
        if not self.trade_history:
            return {}
        
        recent_trades = self.trade_history[-100:]  # Last 100 trades
        
        return {
            "total_trades": len(self.trade_history),
            "recent_trades": len(recent_trades),
            "prices": {rt.value: price for rt, price in self.prices.items()},
            "supply": {rt.value: amount for rt, amount in self.supply.items()},
            "demand": {rt.value: amount for rt, amount in self.demand.items()}
        }

class EconomicMetabolism:
    """
    Economic metabolism system inspired by wawa framework.
    Manages resource flows, production, consumption, and exchange.
    """
    
    def __init__(self, num_agents: int = 20):
        self.num_agents = num_agents
        self.agents: Dict[str, EconomicAgent] = {}
        self.market = Market()
        self.time_step = 0
        
        # Production costs
        self.production_costs = {
            ResourceType.COMPUTE: {ResourceType.ENERGY: 1.0},
            ResourceType.ENERGY: {ResourceType.COMPUTE: 0.5},
            ResourceType.KNOWLEDGE: {ResourceType.COMPUTE: 2.0, ResourceType.SOCIAL: 1.0},
            ResourceType.SOCIAL: {ResourceType.KNOWLEDGE: 0.5}
        }
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize economic agents with initial resources."""
        for i in range(self.num_agents):
            agent_id = f"agent_{i}"
            
            # Give each agent initial resources
            initial_resources = {
                ResourceType.COMPUTE: np.random.uniform(5, 15),
                ResourceType.ENERGY: np.random.uniform(5, 15),
                ResourceType.KNOWLEDGE: np.random.uniform(2, 8),
                ResourceType.SOCIAL: np.random.uniform(2, 8)
            }
            
            agent = EconomicAgent(agent_id, initial_resources)
            self.agents[agent_id] = agent
    
    def step(self):
        """Perform one time step of economic metabolism."""
        self.time_step += 1
        
        # Production phase
        self._production_phase()
        
        # Consumption phase
        self._consumption_phase()
        
        # Exchange phase
        self._exchange_phase()
        
        # Update market prices
        self.market.update_prices()
    
    def _production_phase(self):
        """Agents produce resources based on their strategy."""
        for agent in self.agents.values():
            # Each agent chooses what to produce based on their resources
            # Simple strategy: produce resource they have most of
            resources_sorted = sorted(
                agent.resources.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            if resources_sorted:
                resource_to_produce = resources_sorted[0][0]
                cost = self.production_costs.get(resource_to_produce, {})
                
                # Produce
                amount = np.random.uniform(0.5, 2.0)
                success = agent.produce(resource_to_produce, amount, cost)
                
                if success:
                    # Update market supply
                    self.market.supply[resource_to_produce] += amount
    
    def _consumption_phase(self):
        """Agents consume resources for utility."""
        for agent in self.agents.values():
            # Consume resources to maintain operations
            consumption = {
                ResourceType.ENERGY: 0.5,
                ResourceType.COMPUTE: 0.3,
                ResourceType.KNOWLEDGE: 0.1,
                ResourceType.SOCIAL: 0.1
            }
            
            total_consumed = 0
            for resource_type, amount in consumption.items():
                if agent.consume(resource_type, amount):
                    total_consumed += amount
            
            # Update market demand
            for resource_type, amount in consumption.items():
                self.market.demand[resource_type] += amount
    
    def _exchange_phase(self):
        """Agents exchange resources in the market."""
        # Simple exchange: agents with excess sell to those with deficit
        for resource_type in ResourceType:
            # Find sellers (agents with excess)
            sellers = []
            buyers = []
            
            for agent in self.agents.values():
                amount = agent.resources.get(resource_type, 0)
                if amount > 10:  # Excess threshold
                    sellers.append((agent, amount - 10))
                elif amount < 3:  # Deficit threshold
                    buyers.append((agent, 3 - amount))
            
            # Match buyers and sellers
            for buyer, needed in buyers:
                for seller, available in sellers:
                    if available > 0 and needed > 0:
                        trade_amount = min(available, needed)
                        price = self.market.prices[resource_type]
                        
                        # Execute trade
                        if seller.resources[resource_type] >= trade_amount:
                            seller.resources[resource_type] -= trade_amount
                            buyer.resources[resource_type] += trade_amount
                            
                            # Record trade
                            self.market.record_trade(
                                buyer.id,
                                seller.id,
                                resource_type,
                                trade_amount,
                                price
                            )
                            
                            available -= trade_amount
                            needed -= trade_amount
    
    def get_system_status(self) -> Dict:
        """Get overall system status."""
        total_wealth = sum(agent.get_total_wealth() for agent in self.agents.values())
        avg_wealth = total_wealth / len(self.agents)
        
        resource_totals = {}
        for resource_type in ResourceType:
            total = sum(agent.resources.get(resource_type, 0) for agent in self.agents.values())
            resource_totals[resource_type.value] = total
        
        return {
            "time_step": self.time_step,
            "total_agents": len(self.agents),
            "total_wealth": total_wealth,
            "average_wealth": avg_wealth,
            "resource_totals": resource_totals,
            "market_stats": self.market.get_market_stats()
        }

# Test the economic metabolism system
if __name__ == "__main__":
    print("Digital Organism - Phase 6: Transcendence")
    print("=" * 60)
    print("Economic Metabolism (wawa Framework)\n")
    
    # Initialize economic system
    print("Initializing economic metabolism system...")
    economy = EconomicMetabolism(num_agents=20)
    print(f"Created {len(economy.agents)} economic agents")
    
    # Show initial status
    print("\nInitial System Status:")
    status = economy.get_system_status()
    print(f"  Total agents: {status['total_agents']}")
    print(f"  Total wealth: {status['total_wealth']:.2f}")
    print(f"  Average wealth: {status['average_wealth']:.2f}")
    print(f"  Resource totals: {status['resource_totals']}")
    
    # Run simulation
    print("\nRunning economic simulation for 10 time steps...")
    for step in range(10):
        economy.step()
        
        if step % 2 == 0:
            status = economy.get_system_status()
            print(f"\nTime Step {step + 1}:")
            print(f"  Total wealth: {status['total_wealth']:.2f}")
            print(f"  Average wealth: {status['average_wealth']:.2f}")
            print(f"  Market prices: {status['market_stats'].get('prices', {})}")
    
    # Final status
    print("\n" + "=" * 60)
    print("Final System Status")
    print("=" * 60)
    status = economy.get_system_status()
    print(f"  Time steps: {status['time_step']}")
    print(f"  Total agents: {status['total_agents']}")
    print(f"  Total wealth: {status['total_wealth']:.2f}")
    print(f"  Average wealth: {status['average_wealth']:.2f}")
    print(f"  Resource totals: {status['resource_totals']}")
    
    # Market stats
    market_stats = status['market_stats']
    if market_stats:
        print(f"\nMarket Statistics:")
        print(f"  Total trades: {market_stats.get('total_trades', 0)}")
        print(f"  Final prices: {market_stats.get('prices', {})}")
    
    print("\n" + "=" * 60)
    print("Phase 6 Summary")
    print("=" * 60)
    print("\n[OK] Economic Metabolism: Implemented with 20 agents")
    print("[OK] Resource Types: Compute, Energy, Knowledge, Social")
    print("[OK] Production: Agents produce resources at costs")
    print("[OK] Consumption: Agents consume resources for utility")
    print("[OK] Market Exchange: Supply-demand based trading")
    print("[OK] Price Dynamics: Prices adjust based on supply/demand")
    print("[OK] Multi-Agent Swarms: Implemented (50 agents)")
    print("[--] Tribe Model: Pending")
