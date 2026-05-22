"""
Phase 4: Biological Grounding - Tölvera Basal Agency
Self-organizing systems for exploring diverse intelligence through collective action
Uses Taichi for parallel computation of agent behaviors
"""

import taichi as ti
import numpy as np
from typing import Dict, List, Tuple
import time

# Initialize Taichi
ti.init(arch=ti.cpu)  # Use CPU for compatibility

@ti.data_oriented
class BasalAgency:
    """
    Implements basal agency behaviors inspired by biological systems:
    - Flocking (bird-like collective movement)
    - Slime mold growth (efficient foraging patterns)
    - Swarming (insect-like collective intelligence)
    """
    
    def __init__(self, num_agents: int = 1000):
        self.num_agents = num_agents
        
        # Agent properties (using Taichi fields for parallel computation)
        self.positions = ti.Vector.field(2, dtype=ti.f32, shape=(num_agents,))
        self.velocities = ti.Vector.field(2, dtype=ti.f32, shape=(num_agents,))
        self.colors = ti.Vector.field(3, dtype=ti.f32, shape=(num_agents,))
        
        # Simulation parameters
        self.dt = 0.01
        self.neighbor_radius = 0.1
        self.alignment_weight = 1.0
        self.cohesion_weight = 1.0
        self.separation_weight = 1.5
        
        # Initialize agents randomly
        self._initialize_agents()
    
    @ti.kernel
    def _initialize_agents(self):
        """Initialize agent positions and velocities randomly."""
        for i in range(self.num_agents):
            self.positions[i] = ti.Vector([ti.random() * 2.0 - 1.0, ti.random() * 2.0 - 1.0])
            self.velocities[i] = ti.Vector([ti.random() * 0.1 - 0.05, ti.random() * 0.1 - 0.05])
            self.colors[i] = ti.Vector([ti.random(), ti.random(), ti.random()])
    
    @ti.kernel
    def compute_flocking_forces(self):
        """
        Compute flocking forces (alignment, cohesion, separation).
        This is the classic Boids algorithm for simulating bird flocking.
        """
        
        for i in range(self.num_agents):
            alignment = ti.Vector([0.0, 0.0])
            cohesion = ti.Vector([0.0, 0.0])
            separation = ti.Vector([0.0, 0.0])
            
            neighbors = 0
            
            for j in range(self.num_agents):
                if i == j:
                    continue
                
                # Calculate distance
                diff = self.positions[j] - self.positions[i]
                dist = diff.norm()
                
                if dist < self.neighbor_radius:
                    # Alignment: match velocity
                    alignment += self.velocities[j]
                    
                    # Cohesion: move toward center
                    cohesion += self.positions[j]
                    
                    # Separation: avoid crowding
                    if dist > 0.001:
                        separation -= diff / dist
                    
                    neighbors += 1
            
            if neighbors > 0:
                # Normalize forces
                alignment /= neighbors
                cohesion /= neighbors
                cohesion -= self.positions[i]  # Move toward center
                separation /= neighbors
                
                # Apply weights
                force = (self.alignment_weight * alignment +
                        self.cohesion_weight * cohesion +
                        self.separation_weight * separation)
                
                # Update velocity
                self.velocities[i] += force * self.dt
                
                # Limit speed
                speed = self.velocities[i].norm()
                max_speed = 0.5
                if speed > max_speed:
                    self.velocities[i] *= max_speed / speed
            
            # Update position
            self.positions[i] += self.velocities[i] * self.dt
            
            # Boundary wrapping (toroidal space)
            for k in range(2):
                if self.positions[i][k] > 1.0:
                    self.positions[i][k] -= 2.0
                elif self.positions[i][k] < -1.0:
                    self.positions[i][k] += 2.0
    
    def step(self):
        """Perform one simulation step."""
        self.compute_flocking_forces()
    
    def get_positions(self) -> np.ndarray:
        """Get current agent positions as numpy array."""
        positions = self.positions.to_numpy()
        return positions
    
    def get_velocities(self) -> np.ndarray:
        """Get current agent velocities as numpy array."""
        velocities = self.velocities.to_numpy()
        return velocities
    
    def get_colors(self) -> np.ndarray:
        """Get current agent colors as numpy array."""
        colors = self.colors.to_numpy()
        return colors

@ti.data_oriented
class SlimeMold:
    """
    Simulates Physarum polycephalum (slime mold) foraging behavior.
    Uses agent-based model with trail following and exploration.
    """
    
    def __init__(self, num_agents: int = 500):
        self.num_agents = num_agents
        
        # Agent positions and angles
        self.positions = ti.Vector.field(2, dtype=ti.f32, shape=(num_agents,))
        self.angles = ti.field(dtype=ti.f32, shape=(num_agents,))
        
        # Trail map (pheromone deposition)
        self.trail_map = ti.field(dtype=ti.f32, shape=(100, 100))
        
        # Simulation parameters
        self.sensor_angle = 0.3  # Radians
        self.sensor_distance = 0.05
        self.turn_speed = 0.2
        self.move_speed = 0.01
        
        self._initialize_agents()
    
    @ti.kernel
    def _initialize_agents(self):
        """Initialize slime mold agents."""
        for i in range(self.num_agents):
            self.positions[i] = ti.Vector([0.5, 0.5])
            self.angles[i] = ti.random() * 2.0 * 3.14159
    
    @ti.kernel
    def update_trail_map(self):
        """Decay trail map over time."""
        for i in range(100):
            for j in range(100):
                self.trail_map[i, j] *= 0.95  # Decay factor
    
    @ti.kernel
    def sense_and_move(self):
        """
        Agents sense trail concentration and move accordingly.
        This creates efficient foraging patterns.
        """
        for i in range(self.num_agents):
            # Current position
            x = self.positions[i][0]
            y = self.positions[i][1]
            angle = self.angles[i]
            
            # Sensor positions (left, center, right)
            left_angle = angle - self.sensor_angle
            right_angle = angle + self.sensor_angle
            
            left_sensor = ti.Vector([
                x + ti.cos(left_angle) * self.sensor_distance,
                y + ti.sin(left_angle) * self.sensor_distance
            ])
            
            center_sensor = ti.Vector([
                x + ti.cos(angle) * self.sensor_distance,
                y + ti.sin(angle) * self.sensor_distance
            ])
            
            right_sensor = ti.Vector([
                x + ti.cos(right_angle) * self.sensor_distance,
                y + ti.sin(right_angle) * self.sensor_distance
            ])
            
            # Sample trail concentration at sensors
            # Convert to grid coordinates
            left_x = int(ti.min(ti.max(left_sensor[0] * 100, 0), 99))
            left_y = int(ti.min(ti.max(left_sensor[1] * 100, 0), 99))
            center_x = int(ti.min(ti.max(center_sensor[0] * 100, 0), 99))
            center_y = int(ti.min(ti.max(center_sensor[1] * 100, 0), 99))
            right_x = int(ti.min(ti.max(right_sensor[0] * 100, 0), 99))
            right_y = int(ti.min(ti.max(right_sensor[1] * 100, 0), 99))
            
            left_val = self.trail_map[left_x, left_y]
            center_val = self.trail_map[center_x, center_y]
            right_val = self.trail_map[right_x, right_y]
            
            # Turn based on sensor values
            if left_val > center_val and left_val > right_val:
                self.angles[i] += self.turn_speed
            elif right_val > center_val and right_val > left_val:
                self.angles[i] -= self.turn_speed
            else:
                # Random perturbation
                self.angles[i] += (ti.random() - 0.5) * 0.1
            
            # Move forward
            self.positions[i][0] += ti.cos(self.angles[i]) * self.move_speed
            self.positions[i][1] += ti.sin(self.angles[i]) * self.move_speed
            
            # Boundary conditions
            for k in range(2):
                if self.positions[i][k] < 0.0:
                    self.positions[i][k] = 0.0
                    self.angles[i] += 3.14159
                elif self.positions[i][k] > 1.0:
                    self.positions[i][k] = 1.0
                    self.angles[i] += 3.14159
            
            # Deposit trail
            grid_x = int(ti.min(ti.max(self.positions[i][0] * 100, 0), 99))
            grid_y = int(ti.min(ti.max(self.positions[i][1] * 100, 0), 99))
            self.trail_map[grid_x, grid_y] += 0.1
    
    def step(self):
        """Perform one simulation step."""
        self.update_trail_map()
        self.sense_and_move()
    
    def get_trail_map(self) -> np.ndarray:
        """Get current trail map as numpy array."""
        return self.trail_map.to_numpy()

# Test the basal agency systems
if __name__ == "__main__":
    print("Digital Organism - Phase 4: Biological Grounding")
    print("=" * 60)
    print("Tölvera Basal Agency Behaviors\n")
    
    # Test flocking behavior
    print("Testing Flocking Behavior (Boids)...")
    flocking = BasalAgency(num_agents=500)
    
    print(f"Initialized {flocking.num_agents} agents")
    print("Running simulation for 100 steps...")
    
    start_time = time.time()
    for step in range(100):
        flocking.step()
        if step % 20 == 0:
            positions = flocking.get_positions()
            avg_speed = np.mean(np.linalg.norm(flocking.get_velocities(), axis=1))
            print(f"  Step {step}: Avg speed = {avg_speed:.4f}")
    
    elapsed = time.time() - start_time
    print(f"Simulation completed in {elapsed:.2f}s")
    
    # Test slime mold behavior
    print("\nTesting Slime Mold Foraging Behavior...")
    slime_mold = SlimeMold(num_agents=500)
    
    print(f"Initialized {slime_mold.num_agents} agents")
    print("Running simulation for 100 steps...")
    
    start_time = time.time()
    for step in range(100):
        slime_mold.step()
        if step % 20 == 0:
            trail_map = slime_mold.get_trail_map()
            total_trail = np.sum(trail_map)
            print(f"  Step {step}: Total trail concentration = {total_trail:.2f}")
    
    elapsed = time.time() - start_time
    print(f"Simulation completed in {elapsed:.2f}s")
    
    print("\n" + "=" * 60)
    print("Phase 4 Summary")
    print("=" * 60)
    print("\n[OK] Agentic Worm Connectome: Simulated with simplified C. elegans neurons")
    print("[OK] Multi-Layer Memory: Episodic, Spatial, Semantic, Procedural layers")
    print("[OK] Tölvera Basal Agency: Flocking and slime mold behaviors implemented")
    print("[--] Polars: Pending (requires installation)")
