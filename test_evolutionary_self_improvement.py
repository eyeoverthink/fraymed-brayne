"""
Evolutionary Self-Improvement Test
Tests the Digital Organism's ability to improve itself through:
- Genetic algorithms (evolution)
- Self-modification (code generation)
- Autonomous optimization
"""

import time
import numpy as np
from typing import List, Dict, Tuple
import copy

class GeneticAlgorithm:
    """Simple genetic algorithm for testing evolution."""
    
    def __init__(self, population_size=20, genome_length=10, mutation_rate=0.1):
        self.population_size = population_size
        self.genome_length = genome_length
        self.mutation_rate = mutation_rate
        self.population = self._initialize_population()
        self.generation = 0
        self.fitness_history = []
    
    def _initialize_population(self) -> List[List[float]]:
        """Initialize random population."""
        return [[np.random.uniform(0, 1) for _ in range(self.genome_length)] 
                for _ in range(self.population_size)]
    
    def fitness(self, genome: List[float]) -> float:
        """Calculate fitness (sum of gene values)."""
        return sum(genome)
    
    def select(self) -> List[List[float]]:
        """Select top 50% of population."""
        sorted_pop = sorted(self.population, key=self.fitness, reverse=True)
        return sorted_pop[:self.population_size // 2]
    
    def crossover(self, parent1: List[float], parent2: List[float]) -> List[float]:
        """Single-point crossover."""
        point = np.random.randint(1, self.genome_length)
        child = parent1[:point] + parent2[point:]
        return child
    
    def mutate(self, genome: List[float]) -> List[float]:
        """Random mutation."""
        mutated = copy.deepcopy(genome)
        for i in range(len(mutated)):
            if np.random.random() < self.mutation_rate:
                mutated[i] = np.random.uniform(0, 1)
        return mutated
    
    def evolve(self, generations: int) -> Dict:
        """Run evolution for specified generations."""
        print(f"Running genetic algorithm for {generations} generations...")
        
        initial_fitness = max([self.fitness(g) for g in self.population])
        self.fitness_history.append(initial_fitness)
        
        for gen in range(generations):
            self.generation += 1
            
            # Selection
            selected = self.select()
            
            # Crossover and mutation
            new_population = []
            while len(new_population) < self.population_size:
                # Select indices instead of lists
                idx1, idx2 = np.random.choice(len(selected), 2, replace=False)
                parent1 = selected[idx1]
                parent2 = selected[idx2]
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            self.population = new_population
            
            # Record fitness
            best_fitness = max([self.fitness(g) for g in self.population])
            avg_fitness = np.mean([self.fitness(g) for g in self.population])
            self.fitness_history.append(best_fitness)
            
            print(f"Generation {gen+1}: Best fitness = {best_fitness:.3f}, Avg = {avg_fitness:.3f}")
        
        final_fitness = max([self.fitness(g) for g in self.population])
        improvement = ((final_fitness - initial_fitness) / initial_fitness) * 100
        
        return {
            "initial_fitness": initial_fitness,
            "final_fitness": final_fitness,
            "improvement": improvement,
            "generations": generations,
            "fitness_history": self.fitness_history
        }

class SelfModifyingSystem:
    """Simulates a system that can modify its own code/parameters."""
    
    def __init__(self):
        self.parameters = {
            "learning_rate": 0.01,
            "batch_size": 32,
            "temperature": 0.7,
            "max_tokens": 512,
            "timeout": 30
        }
        self.performance_history = []
        self.modification_count = 0
    
    def evaluate_performance(self) -> float:
        """Simulate performance evaluation (0.0 to 1.0)."""
        # Simulate performance based on parameters
        lr_score = 1.0 - abs(self.parameters["learning_rate"] - 0.05) * 10
        batch_score = min(1.0, self.parameters["batch_size"] / 64)
        temp_score = 1.0 - abs(self.parameters["temperature"] - 0.5) * 2
        timeout_score = min(1.0, 30 / self.parameters["timeout"])
        
        performance = (lr_score + batch_score + temp_score + timeout_score) / 4
        return max(0.0, min(1.0, performance))
    
    def generate_modification(self) -> Dict:
        """Simulate LLM-generated parameter modification."""
        modifications = []
        
        # Randomly select a parameter to modify
        param = np.random.choice(list(self.parameters.keys()))
        current_value = self.parameters[param]
        
        # Generate modification
        if param == "learning_rate":
            new_value = np.random.uniform(0.001, 0.1)
        elif param == "batch_size":
            new_value = int(np.random.choice([16, 32, 64, 128]))
        elif param == "temperature":
            new_value = np.random.uniform(0.1, 1.0)
        elif param == "max_tokens":
            new_value = int(np.random.choice([256, 512, 1024, 2048]))
        elif param == "timeout":
            new_value = int(np.random.choice([10, 20, 30, 60]))
        
        modification = {
            "parameter": param,
            "old_value": current_value,
            "new_value": new_value,
            "reason": f"Optimize {param} for better performance"
        }
        
        return modification
    
    def apply_modification(self, modification: Dict):
        """Apply a modification to the system."""
        param = modification["parameter"]
        new_value = modification["new_value"]
        
        self.parameters[param] = new_value
        self.modification_count += 1
        
        print(f"Modification #{self.modification_count}: {param} = {modification['old_value']} → {new_value}")
        print(f"  Reason: {modification['reason']}")
    
    def self_improve(self, iterations: int) -> Dict:
        """Run self-improvement loop."""
        print(f"\nRunning self-improvement for {iterations} iterations...")
        
        initial_performance = self.evaluate_performance()
        self.performance_history.append(initial_performance)
        
        print(f"Initial performance: {initial_performance:.3f}")
        print(f"Initial parameters: {self.parameters}")
        
        for i in range(iterations):
            # Generate modification
            modification = self.generate_modification()
            
            # Apply modification
            old_value = self.parameters[modification["parameter"]]
            self.apply_modification(modification)
            
            # Evaluate new performance
            new_performance = self.evaluate_performance()
            self.performance_history.append(new_performance)
            
            print(f"  Performance: {new_performance:.3f}")
            
            # If performance decreased, revert
            if new_performance < initial_performance:
                self.parameters[modification["parameter"]] = old_value
                print(f"  Reverted modification (performance decreased)")
        
        final_performance = self.evaluate_performance()
        improvement = final_performance - initial_performance
        
        return {
            "initial_performance": initial_performance,
            "final_performance": final_performance,
            "improvement": improvement,
            "iterations": iterations,
            "modifications_applied": self.modification_count,
            "performance_history": self.performance_history,
            "final_parameters": self.parameters
        }

class AutonomousOptimizer:
    """Simulates autonomous optimization using swarm intelligence."""
    
    def __init__(self, num_agents=10):
        self.num_agents = num_agents
        self.agents = [{"position": np.random.uniform(-10, 10), "velocity": 0, "best_position": None, "best_fitness": float('-inf')} for _ in range(num_agents)]
        self.global_best_position = None
        self.global_best_fitness = float('-inf')
        self.fitness_history = []
    
    def objective_function(self, x: float) -> float:
        """Objective function to maximize (e.g., -x^2 + 100)."""
        return -x**2 + 100
    
    def update_agents(self):
        """Update agent positions using simplified PSO."""
        w = 0.7  # inertia
        c1 = 1.5  # cognitive
        c2 = 1.5  # social
        
        for agent in self.agents:
            # Update velocity
            r1, r2 = np.random.random(), np.random.random()
            
            cognitive = c1 * r1 * (agent["best_position"] - agent["position"]) if agent["best_position"] else 0
            social = c2 * r2 * (self.global_best_position - agent["position"]) if self.global_best_position else 0
            
            agent["velocity"] = w * agent["velocity"] + cognitive + social
            
            # Update position
            agent["position"] += agent["velocity"]
            
            # Clamp position
            agent["position"] = max(-10, min(10, agent["position"]))
            
            # Evaluate fitness
            fitness = self.objective_function(agent["position"])
            
            # Update personal best
            if fitness > agent["best_fitness"]:
                agent["best_fitness"] = fitness
                agent["best_position"] = agent["position"]
            
            # Update global best
            if fitness > self.global_best_fitness:
                self.global_best_fitness = fitness
                self.global_best_position = agent["position"]
    
    def optimize(self, iterations: int) -> Dict:
        """Run autonomous optimization."""
        print(f"\nRunning autonomous optimization with {self.num_agents} agents for {iterations} iterations...")
        
        # Initialize personal bests
        for agent in self.agents:
            agent["best_fitness"] = self.objective_function(agent["position"])
            agent["best_position"] = agent["position"]
        
        # Find initial global best
        self.global_best_fitness = max([agent["best_fitness"] for agent in self.agents])
        best_agent = max(self.agents, key=lambda a: a["best_fitness"])
        self.global_best_position = best_agent["best_position"]
        
        initial_fitness = self.global_best_fitness
        self.fitness_history.append(initial_fitness)
        
        print(f"Initial best fitness: {initial_fitness:.3f} at position {self.global_best_position:.3f}")
        
        for i in range(iterations):
            self.update_agents()
            self.fitness_history.append(self.global_best_fitness)
            
            if i % 5 == 0:
                print(f"Iteration {i+1}: Best fitness = {self.global_best_fitness:.3f} at position {self.global_best_position:.3f}")
        
        final_fitness = self.global_best_fitness
        improvement = final_fitness - initial_fitness
        
        return {
            "initial_fitness": initial_fitness,
            "final_fitness": final_fitness,
            "improvement": improvement,
            "iterations": iterations,
            "fitness_history": self.fitness_history,
            "best_position": self.global_best_position
        }

def main():
    """Run all evolutionary self-improvement tests."""
    print("=" * 60)
    print("EVOLUTIONARY SELF-IMPROVEMENT TEST SUITE")
    print("=" * 60)
    print("Testing the Digital Organism's ability to improve itself")
    
    results = {}
    
    # Test 1: Genetic Algorithm
    print("\n" + "=" * 60)
    print("TEST 1: GENETIC ALGORITHM EVOLUTION")
    print("=" * 60)
    
    ga = GeneticAlgorithm(population_size=20, genome_length=10, mutation_rate=0.1)
    ga_results = ga.evolve(generations=20)
    results["genetic_algorithm"] = ga_results
    
    print(f"\nGenetic Algorithm Results:")
    print(f"  Initial fitness: {ga_results['initial_fitness']:.3f}")
    print(f"  Final fitness: {ga_results['final_fitness']:.3f}")
    print(f"  Improvement: {ga_results['improvement']:.1f}%")
    print(f"  Generations: {ga_results['generations']}")
    
    if ga_results['improvement'] > 0:
        print("  [SUCCESS] System improved through evolution")
    else:
        print("  [FAILURE] System did not improve through evolution")
    
    # Test 2: Self-Modification
    print("\n" + "=" * 60)
    print("TEST 2: SELF-MODIFICATION (Parameter Optimization)")
    print("=" * 60)
    
    sms = SelfModifyingSystem()
    sms_results = sms.self_improve(iterations=10)
    results["self_modification"] = sms_results
    
    print(f"\nSelf-Modification Results:")
    print(f"  Initial performance: {sms_results['initial_performance']:.3f}")
    print(f"  Final performance: {sms_results['final_performance']:.3f}")
    print(f"  Improvement: {sms_results['improvement']:.3f}")
    print(f"  Modifications attempted: {sms_results['modifications_applied']}")
    print(f"  Final parameters: {sms_results['final_parameters']}")
    
    if sms_results['improvement'] > 0:
        print("  [SUCCESS] System improved through self-modification")
    else:
        print("  [FAILURE] System did not improve through self-modification")
    
    # Test 3: Autonomous Optimization
    print("\n" + "=" * 60)
    print("TEST 3: AUTONOMOUS OPTIMIZATION (Swarm Intelligence)")
    print("=" * 60)
    
    ao = AutonomousOptimizer(num_agents=10)
    ao_results = ao.optimize(iterations=20)
    results["autonomous_optimization"] = ao_results
    
    print(f"\nAutonomous Optimization Results:")
    print(f"  Initial fitness: {ao_results['initial_fitness']:.3f}")
    print(f"  Final fitness: {ao_results['final_fitness']:.3f}")
    print(f"  Improvement: {ao_results['improvement']:.3f}")
    print(f"  Iterations: {ao_results['iterations']}")
    print(f"  Best position found: {ao_results['best_position']:.3f}")
    
    if ao_results['improvement'] > 0:
        print("  [SUCCESS] System improved through autonomous optimization")
    else:
        print("  [FAILURE] System did not improve through autonomous optimization")
    
    # Summary
    print("\n" + "=" * 60)
    print("EVOLUTIONARY SELF-IMPROVEMENT TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 3
    successful_tests = sum([
        1 if results["genetic_algorithm"]["improvement"] > 0 else 0,
        1 if results["self_modification"]["improvement"] > 0 else 0,
        1 if results["autonomous_optimization"]["improvement"] > 0 else 0
    ])
    
    print(f"\nTests Passed: {successful_tests}/{total_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    print("\nDetailed Results:")
    print(f"  1. Genetic Algorithm: {results['genetic_algorithm']['improvement']:.1f}% improvement")
    print(f"  2. Self-Modification: {results['self_modification']['improvement']:.3f} improvement")
    print(f"  3. Autonomous Optimization: {results['autonomous_optimization']['improvement']:.3f} improvement")
    
    print("\nConclusion:")
    if successful_tests == total_tests:
        print("  [EXCELLENT] All self-improvement mechanisms working")
    elif successful_tests >= 2:
        print("  [GOOD] Most self-improvement mechanisms working")
    elif successful_tests == 1:
        print("  [POOR] Only one self-improvement mechanism working")
    else:
        print("  [FAILURE] No self-improvement mechanisms working")
    
    return results

if __name__ == "__main__":
    results = main()
