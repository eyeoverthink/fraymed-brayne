"""
Phase 4: Biological Grounding - Agentic Worm Connectome Simulation
Based on C. elegans nematode (302 neurons from OpenWorm)
Implements biological neural network simulation for grounding AI in biological principles
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import time
import json

class Neuron:
    """Represents a single neuron in the connectome."""
    
    def __init__(self, neuron_id: str, neuron_type: str):
        self.id = neuron_id
        self.type = neuron_type  # sensory, interneuron, motor
        self.membrane_potential = 0.0
        self.threshold = -55.0  # mV
        self.resting_potential = -70.0  # mV
        self.firing = False
        self.last_spike_time = 0.0
        self.connections = []  # List of (target_neuron, weight, delay)
    
    def update_potential(self, input_current: float, dt: float = 0.1):
        """Update membrane potential based on input current."""
        # Leak current
        leak_conductance = 0.1
        leak_current = leak_conductance * (self.membrane_potential - self.resting_potential)
        
        # Update potential
        self.membrane_potential += (input_current - leak_current) * dt
        
        # Check for spike
        if self.membrane_potential >= self.threshold:
            self.firing = True
            self.last_spike_time = time.time()
            self.membrane_potential = self.resting_potential  # Reset after spike
        else:
            self.firing = False
    
    def reset(self):
        """Reset neuron to resting state."""
        self.membrane_potential = self.resting_potential
        self.firing = False

class Connectome:
    """
    Simulates the C. elegans connectome with 302 neurons.
    Implements biological neural network principles for grounding.
    """
    
    def __init__(self):
        self.neurons: Dict[str, Neuron] = {}
        self.synaptic_weights = {}  # (pre, post) -> weight
        self.neurotransmitters = {}  # neuron -> neurotransmitter type
        self.sensory_inputs = {}  # sensory neuron -> input value
        self.motor_outputs = {}  # motor neuron -> output value
        
        # Initialize simplified connectome
        self._initialize_connectome()
    
    def _initialize_connectome(self):
        """
        Initialize a simplified version of C. elegans connectome.
        Full connectome has 302 neurons and ~5000 synapses.
        This is a simplified model for demonstration.
        """
        # Sensory neurons (detect environmental stimuli)
        sensory_neurons = [
            "ASEL", "ASER",  # Chemotaxis (salt)
            "AWCL", "AWCR",  # Odor sensing
            "PLML", "PLMR",  # Touch
            "FLPL", "FPR",   # Temperature
        ]
        
        # Interneurons (process information)
        interneurons = [
            "AIBL", "AIBR",  # Integration
            "AIYL", "AIYR",  # Navigation
            "RIML", "RIMR",  # Motor control
            "AVBL", "AVBR",  # Command
        ]
        
        # Motor neurons (control movement)
        motor_neurons = [
            "AVAL", "AVAR",  # Backward movement
            "AVBL", "AVBR",  # Forward movement
            "VB01", "VB02",  # Ventral cord
        ]
        
        # Create neurons
        for neuron_id in sensory_neurons:
            self.neurons[neuron_id] = Neuron(neuron_id, "sensory")
        
        for neuron_id in interneurons:
            self.neurons[neuron_id] = Neuron(neuron_id, "interneuron")
        
        for neuron_id in motor_neurons:
            self.neurons[neuron_id] = Neuron(neuron_id, "motor")
        
        # Create simplified synaptic connections
        # In reality, these would be based on actual C. elegans connectome data
        self._create_connections(sensory_neurons, interneurons, motor_neurons)
    
    def _create_connections(self, sensory: List[str], interneurons: List[str], motor: List[str]):
        """Create synaptic connections between neurons."""
        # Sensory to interneuron connections
        for s in sensory:
            for i in interneurons[:3]:  # Connect to first few interneurons
                weight = np.random.uniform(0.5, 2.0)
                self.neurons[s].connections.append((i, weight, 1.0))
        
        # Interneuron to interneuron connections
        for i1 in interneurons:
            for i2 in interneurons:
                if i1 != i2 and np.random.random() > 0.7:
                    weight = np.random.uniform(-1.0, 1.0)
                    self.neurons[i1].connections.append((i2, weight, 0.5))
        
        # Interneuron to motor connections
        for i in interneurons:
            for m in motor:
                if np.random.random() > 0.6:
                    weight = np.random.uniform(0.5, 2.0)
                    self.neurons[i].connections.append((m, weight, 0.3))
    
    def stimulate_sensory(self, sensory_neuron: str, intensity: float):
        """Stimulate a sensory neuron with given intensity."""
        if sensory_neuron in self.neurons:
            self.sensory_inputs[sensory_neuron] = intensity
    
    def step(self, dt: float = 0.1):
        """Simulate one time step of neural activity."""
        # Reset motor outputs
        self.motor_outputs = {}
        
        # Update each neuron
        for neuron_id, neuron in self.neurons.items():
            input_current = 0.0
            
            # Sensory input
            if neuron.type == "sensory" and neuron_id in self.sensory_inputs:
                input_current += self.sensory_inputs[neuron_id]
            
            # Synaptic inputs from firing neurons
            for target_id, weight, delay in neuron.connections:
                if self.neurons[target_id].firing:
                    input_current += weight
            
            # Update potential
            neuron.update_potential(input_current, dt)
            
            # Record motor outputs
            if neuron.type == "motor" and neuron.firing:
                self.motor_outputs[neuron_id] = neuron.membrane_potential
    
    def get_behavior(self) -> Dict:
        """Determine behavior based on motor neuron activity."""
        behavior = {
            "forward": 0.0,
            "backward": 0.0,
            "turn": 0.0,
            "speed": 0.0
        }
        
        # Calculate motor activity
        forward_neurons = ["AVBL", "AVBR", "VB01", "VB02"]
        backward_neurons = ["AVAL", "AVAR"]
        
        for neuron_id in forward_neurons:
            if neuron_id in self.motor_outputs:
                behavior["forward"] += self.motor_outputs[neuron_id]
        
        for neuron_id in backward_neurons:
            if neuron_id in self.motor_outputs:
                behavior["backward"] += self.motor_outputs[neuron_id]
        
        # Normalize
        total = behavior["forward"] + behavior["backward"]
        if total > 0:
            behavior["speed"] = total / 10.0
            behavior["forward"] /= total
            behavior["backward"] /= total
        
        return behavior
    
    def reset(self):
        """Reset all neurons to resting state."""
        for neuron in self.neurons.values():
            neuron.reset()
        self.sensory_inputs = {}
        self.motor_outputs = {}

class MultiLayerMemory:
    """
    Multi-layer memory system inspired by biological memory:
    - Episodic: Location-action-outcome pairs
    - Spatial: Environmental heatmaps
    - Semantic: Generalized knowledge extraction
    - Procedural: Behavioral strategy storage
    """
    
    def __init__(self):
        self.episodic_memory = []  # List of episodic events
        self.spatial_memory = {}  # Location -> features
        self.semantic_memory = {}  # Concept -> knowledge
        self.procedural_memory = {}  # Task -> strategy
        
    def store_episodic(self, location: str, action: str, outcome: str, reward: float):
        """Store an episodic memory (what, where, when, outcome)."""
        event = {
            "timestamp": time.time(),
            "location": location,
            "action": action,
            "outcome": outcome,
            "reward": reward
        }
        self.episodic_memory.append(event)
        
        # Also update spatial memory
        if location not in self.spatial_memory:
            self.spatial_memory[location] = {"visits": 0, "actions": [], "avg_reward": 0.0}
        
        self.spatial_memory[location]["visits"] += 1
        self.spatial_memory[location]["actions"].append(action)
        
        # Update average reward
        n = self.spatial_memory[location]["visits"]
        old_avg = self.spatial_memory[location]["avg_reward"]
        self.spatial_memory[location]["avg_reward"] = (old_avg * (n-1) + reward) / n
    
    def store_semantic(self, concept: str, knowledge: str, confidence: float = 1.0):
        """Store semantic knowledge (general facts)."""
        if concept not in self.semantic_memory:
            self.semantic_memory[concept] = []
        
        self.semantic_memory[concept].append({
            "knowledge": knowledge,
            "confidence": confidence,
            "timestamp": time.time()
        })
    
    def store_procedural(self, task: str, strategy: str, success_rate: float):
        """Store procedural memory (how to do things)."""
        self.procedural_memory[task] = {
            "strategy": strategy,
            "success_rate": success_rate,
            "timestamp": time.time()
        }
    
    def retrieve_episodic(self, location: str = None, action: str = None) -> List[Dict]:
        """Retrieve episodic memories matching criteria."""
        results = []
        for event in self.episodic_memory:
            match = True
            if location and event["location"] != location:
                match = False
            if action and event["action"] != action:
                match = False
            if match:
                results.append(event)
        return results
    
    def retrieve_semantic(self, concept: str) -> List[Dict]:
        """Retrieve semantic knowledge about a concept."""
        return self.semantic_memory.get(concept, [])
    
    def retrieve_procedural(self, task: str) -> Optional[Dict]:
        """Retrieve procedural strategy for a task."""
        return self.procedural_memory.get(task)
    
    def get_memory_summary(self) -> Dict:
        """Get summary of memory contents."""
        return {
            "episodic_count": len(self.episodic_memory),
            "spatial_locations": len(self.spatial_memory),
            "semantic_concepts": len(self.semantic_memory),
            "procedural_tasks": len(self.procedural_memory)
        }

# Test the biological grounding systems
if __name__ == "__main__":
    print("Digital Organism - Phase 4: Biological Grounding")
    print("=" * 60)
    print("Agentic Worm Connectome Simulation\n")
    
    # Initialize connectome
    print("Initializing C. elegans connectome simulation...")
    connectome = Connectome()
    print(f"Created {len(connectome.neurons)} neurons")
    
    # Initialize multi-layer memory
    print("\nInitializing multi-layer memory system...")
    memory = MultiLayerMemory()
    
    print("\n" + "=" * 60)
    print("Testing Connectome Simulation")
    print("=" * 60)
    
    # Simulate chemotaxis (attraction to salt)
    print("\nSimulating chemotaxis behavior (salt attraction)...")
    
    # Stimulate salt-sensing neurons
    connectome.stimulate_sensory("ASEL", 2.0)  # Left salt sensor
    connectome.stimulate_sensory("ASER", 1.0)  # Right salt sensor (less intense)
    
    # Run simulation steps
    for step in range(10):
        connectome.step()
        behavior = connectome.get_behavior()
        print(f"Step {step+1}: Forward={behavior['forward']:.2f}, Backward={behavior['backward']:.2f}, Speed={behavior['speed']:.2f}")
    
    print("\n" + "=" * 60)
    print("Testing Multi-Layer Memory")
    print("=" * 60)
    
    # Store episodic memories
    print("\nStoring episodic memories...")
    memory.store_episodic("location_A", "move_forward", "found_food", 1.0)
    memory.store_episodic("location_B", "turn_left", "found_food", 0.8)
    memory.store_episodic("location_C", "move_backward", "danger", -0.5)
    
    # Store semantic knowledge
    print("Storing semantic knowledge...")
    memory.store_semantic("salt", "Chemical that attracts C. elegans")
    memory.store_semantic("food", "Source of energy and reward")
    
    # Store procedural memory
    print("Storing procedural strategies...")
    memory.store_procedural("find_food", "follow_chemical_gradient", 0.9)
    memory.store_procedural("avoid_danger", "move_backward", 0.85)
    
    # Retrieve memories
    print("\nRetrieving episodic memories from location_A...")
    episodic = memory.retrieve_episodic(location="location_A")
    for event in episodic:
        print(f"  Action: {event['action']}, Outcome: {event['outcome']}, Reward: {event['reward']}")
    
    print("\nRetrieving semantic knowledge about 'salt'...")
    semantic = memory.retrieve_semantic("salt")
    for item in semantic:
        print(f"  Knowledge: {item['knowledge']}, Confidence: {item['confidence']}")
    
    print("\nRetrieving procedural strategy for 'find_food'...")
    procedural = memory.retrieve_procedural("find_food")
    if procedural:
        print(f"  Strategy: {procedural['strategy']}, Success Rate: {procedural['success_rate']}")
    
    # Memory summary
    print("\n" + "=" * 60)
    print("Memory Summary")
    print("=" * 60)
    summary = memory.get_memory_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("Phase 4 Summary")
    print("=" * 60)
    print("\n[OK] Agentic Worm Connectome: Simulated with simplified C. elegans neurons")
    print("[OK] Multi-Layer Memory: Episodic, Spatial, Semantic, Procedural layers")
    print("[--] Tölvera: Pending (requires Taichi library)")
    print("[--] Polars: Pending (requires installation)")
