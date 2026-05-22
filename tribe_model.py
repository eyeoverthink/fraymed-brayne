"""
Phase 6: Transcendence - Tribe Model for Multi-Generational Learning
Implements tribe-based learning across generations with cultural transmission
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import time
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class KnowledgeFragment:
    """A piece of knowledge that can be transmitted across generations."""
    id: str
    content: str
    value: float
    origin_generation: int
    transmission_count: int = 0
    last_used: float = 0.0

@dataclass
class Individual:
    """An individual in the tribe."""
    id: str
    generation: int
    knowledge: Dict[str, KnowledgeFragment] = field(default_factory=dict)
    performance: float = 0.5
    parent_ids: List[str] = field(default_factory=list)
    
    def learn(self, knowledge_fragment: KnowledgeFragment):
        """Learn a knowledge fragment."""
        knowledge_fragment.transmission_count += 1
        knowledge_fragment.last_used = time.time()
        self.knowledge[knowledge_fragment.id] = knowledge_fragment
    
    def forget(self, knowledge_id: str):
        """Forget a knowledge fragment."""
        if knowledge_id in self.knowledge:
            del self.knowledge[knowledge_id]
    
    def get_knowledge_value(self) -> float:
        """Calculate total value of knowledge."""
        return sum(kf.value for kf in self.knowledge.values())

class Tribe:
    """
    Tribe model for multi-generational learning.
    Implements cultural transmission and knowledge evolution across generations.
    """
    
    def __init__(self, initial_population: int = 20):
        self.current_generation = 0
        self.individuals: Dict[str, Individual] = {}
        self.knowledge_base: Dict[str, KnowledgeFragment] = {}
        self.generation_history: List[Dict] = []
        self.max_individuals = 50
        
        # Cultural transmission parameters
        self.transmission_rate = 0.7  # Probability of knowledge transmission
        self.mutation_rate = 0.1  # Probability of knowledge mutation
        self.forgetting_rate = 0.05  # Probability of forgetting knowledge
        self.generation_size = 20  # Number of individuals per generation
        
        # Initialize first generation
        self._initialize_generation(initial_population)
    
    def _initialize_generation(self, population: int):
        """Initialize the first generation with random knowledge."""
        for i in range(population):
            individual_id = f"gen0_ind{i}"
            individual = Individual(
                id=individual_id,
                generation=0,
                performance=np.random.uniform(0.3, 0.7)
            )
            
            # Give each individual some initial knowledge
            num_knowledge = np.random.randint(3, 8)
            for j in range(num_knowledge):
                knowledge_id = f"knowledge_{len(self.knowledge_base)}"
                knowledge = KnowledgeFragment(
                    id=knowledge_id,
                    content=f"Initial knowledge {j}",
                    value=np.random.uniform(0.5, 1.0),
                    origin_generation=0
                )
                self.knowledge_base[knowledge_id] = knowledge
                individual.learn(knowledge)
            
            self.individuals[individual_id] = individual
        
        self.current_generation = 0
    
    def next_generation(self):
        """Create the next generation from current individuals."""
        self.current_generation += 1
        
        # Select parents based on performance
        sorted_individuals = sorted(
            self.individuals.values(),
            key=lambda ind: ind.performance,
            reverse=True
        )
        
        # Select top performers as parents
        num_parents = max(2, len(sorted_individuals) // 2)
        parents = sorted_individuals[:num_parents]
        
        # Create new generation
        new_individuals = {}
        for i in range(self.generation_size):
            # Select parents
            parent1, parent2 = np.random.choice(parents, 2, replace=False)
            
            # Create offspring
            offspring_id = f"gen{self.current_generation}_ind{i}"
            offspring = Individual(
                id=offspring_id,
                generation=self.current_generation,
                performance=0.5,  # Initial performance
                parent_ids=[parent1.id, parent2.id]
            )
            
            # Cultural transmission from parents
            self._cultural_transmission(offspring, parent1, parent2)
            
            # Mutation
            self._knowledge_mutation(offspring)
            
            # Forgetting
            self._knowledge_forgetting(offspring)
            
            new_individuals[offspring_id] = offspring
        
        # Replace old generation
        self.individuals = new_individuals
        
        # Record generation history
        self._record_generation_history()
    
    def _cultural_transmission(self, offspring: Individual, parent1: Individual, parent2: Individual):
        """Transmit knowledge from parents to offspring."""
        # Combine knowledge from both parents
        parent_knowledge = list(parent1.knowledge.values()) + list(parent2.knowledge.values())
        
        for knowledge in parent_knowledge:
            # Transmission probability
            if np.random.random() < self.transmission_rate:
                # Create copy of knowledge (to track transmission)
                knowledge_copy = deepcopy(knowledge)
                offspring.learn(knowledge_copy)
    
    def _knowledge_mutation(self, individual: Individual):
        """Mutate knowledge (create new knowledge or modify existing)."""
        # Create new knowledge
        if np.random.random() < self.mutation_rate:
            knowledge_id = f"knowledge_{len(self.knowledge_base)}"
            knowledge = KnowledgeFragment(
                id=knowledge_id,
                content=f"Mutated knowledge gen{self.current_generation}",
                value=np.random.uniform(0.3, 1.2),
                origin_generation=self.current_generation
            )
            self.knowledge_base[knowledge_id] = knowledge
            individual.learn(knowledge)
        
        # Modify existing knowledge
        for knowledge_id, knowledge in individual.knowledge.items():
            if np.random.random() < self.mutation_rate * 0.5:
                knowledge.value *= np.random.uniform(0.8, 1.2)
                knowledge.value = max(0.1, min(2.0, knowledge.value))
    
    def _knowledge_forgetting(self, individual: Individual):
        """Forget less valuable knowledge."""
        knowledge_ids = list(individual.knowledge.keys())
        
        for knowledge_id in knowledge_ids:
            knowledge = individual.knowledge[knowledge_id]
            
            # Higher probability to forget low-value knowledge
            forget_probability = self.forgetting_rate * (1.0 - knowledge.value)
            
            if np.random.random() < forget_probability:
                individual.forget(knowledge_id)
    
    def evaluate_individuals(self):
        """Evaluate individual performance based on knowledge."""
        for individual in self.individuals.values():
            # Performance based on knowledge value and diversity
            knowledge_value = individual.get_knowledge_value()
            knowledge_diversity = len(individual.knowledge)
            
            # Calculate performance
            performance = (knowledge_value * 0.7) + (knowledge_diversity * 0.03)
            performance = max(0.1, min(1.0, performance))
            
            individual.performance = performance
    
    def _record_generation_history(self):
        """Record statistics for the current generation."""
        avg_performance = np.mean([ind.performance for ind in self.individuals.values()])
        total_knowledge = len(self.knowledge_base)
        avg_knowledge_per_individual = np.mean([len(ind.knowledge) for ind in self.individuals.values()])
        
        generation_stats = {
            "generation": self.current_generation,
            "population_size": len(self.individuals),
            "average_performance": avg_performance,
            "total_knowledge": total_knowledge,
            "avg_knowledge_per_individual": avg_knowledge_per_individual,
            "timestamp": time.time()
        }
        
        self.generation_history.append(generation_stats)
    
    def get_tribe_status(self) -> Dict:
        """Get current tribe status."""
        avg_performance = np.mean([ind.performance for ind in self.individuals.values()])
        
        return {
            "current_generation": self.current_generation,
            "population_size": len(self.individuals),
            "total_knowledge": len(self.knowledge_base),
            "average_performance": avg_performance,
            "generations_completed": len(self.generation_history)
        }

# Test the tribe model
if __name__ == "__main__":
    print("Digital Organism - Phase 6: Transcendence")
    print("=" * 60)
    print("Tribe Model for Multi-Generational Learning\n")
    
    # Initialize tribe
    print("Initializing tribe...")
    tribe = Tribe(initial_population=20)
    print(f"Created generation 0 with {len(tribe.individuals)} individuals")
    
    # Show initial status
    print("\nInitial Tribe Status:")
    status = tribe.get_tribe_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Run simulation for multiple generations
    print("\nRunning multi-generational simulation...")
    for generation in range(10):
        print(f"\n--- Generation {generation} ---")
        
        # Evaluate current generation
        tribe.evaluate_individuals()
        
        # Show status before next generation
        status = tribe.get_tribe_status()
        print(f"  Population: {status['population_size']}")
        print(f"  Average performance: {status['average_performance']:.3f}")
        print(f"  Total knowledge: {status['total_knowledge']}")
        
        # Create next generation
        if generation < 9:  # Don't create generation after last one
            tribe.next_generation()
    
    # Final status
    print("\n" + "=" * 60)
    print("Final Tribe Status")
    print("=" * 60)
    status = tribe.get_tribe_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show generation history
    print("\nGeneration History:")
    for gen_stats in tribe.generation_history:
        print(f"  Gen {gen_stats['generation']}: Perf={gen_stats['average_performance']:.3f}, "
              f"Knowledge={gen_stats['total_knowledge']}, "
              f"Avg Knowledge/Ind={gen_stats['avg_knowledge_per_individual']:.2f}")
    
    # Calculate improvement
    if len(tribe.generation_history) >= 2:
        initial_perf = tribe.generation_history[0]['average_performance']
        final_perf = tribe.generation_history[-1]['average_performance']
        improvement = ((final_perf - initial_perf) / initial_perf) * 100
        print(f"\nPerformance Improvement: {improvement:.1f}%")
    
    print("\n" + "=" * 60)
    print("Phase 6 Summary")
    print("=" * 60)
    print("\n[OK] Multi-Agent Swarms: Implemented (50 agents)")
    print("[OK] Economic Metabolism: Implemented (20 agents, 4 resource types)")
    print("[OK] Tribe Model: Implemented with multi-generational learning")
    print("[OK] Cultural Transmission: Knowledge inheritance from parents")
    print("[OK] Knowledge Mutation: Innovation through variation")
    print("[OK] Knowledge Forgetting: Pruning of low-value knowledge")
    print("[OK] Performance Evaluation: Fitness-based selection")
    print("[--] Phase Transition: Pending")
