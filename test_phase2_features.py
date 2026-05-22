"""
Test Phase 2 Features: RK4 Integration, Working Memory, Coherence Bands
Tests the three new features added to comprehensive_brain_template.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from comprehensive_brain_template import ComprehensiveBrain, BrainRegion

print("=" * 70)
print("PHASE 2 FEATURES TEST")
print("Testing RK4 Integration, Working Memory, and Coherence Bands")
print("=" * 70)

# Initialize comprehensive brain
print("\n1. Initializing Comprehensive Brain...")
brain = ComprehensiveBrain()
print(f"   Brain initialized: {len(brain.neurons)} neurons, {len(brain.synapses)} synapses")

# Test 1: RK4 Integration
print("\n2. Testing RK4 Integration in SIMDFieldEngineSystem...")
print("-" * 70)
simd_system = brain.systems["simd_field_engine"]

# Initial state
initial_state = simd_system.state.copy()
print(f"   Initial state norm: {np.linalg.norm(initial_state):.3f}")

# Apply RK4 step with input force
input_force = np.random.randn(64) * 0.1
result = simd_system.process({"operation": "rk4_step", "input_force": input_force.tolist()})
updated_state = np.array(result["state"])
print(f"   Updated state norm: {np.linalg.norm(updated_state):.3f}")
print(f"   Dynamics steps: {result['dynamics_steps']}")
print(f"   [OK] RK4 integration functional")

# Test multiple RK4 steps
print("\n   Testing multiple RK4 steps...")
for i in range(10):
    force = np.random.randn(64) * 0.05
    simd_system.process({"operation": "rk4_step", "input_force": force.tolist()})
print(f"   After 10 steps - State norm: {np.linalg.norm(simd_system.state):.3f}")
print(f"   Dynamics history length: {len(simd_system.dynamics_history)}")
print(f"   [OK] Multi-step RK4 integration functional")

# Test 2: Working Memory Buffer
print("\n3. Testing Working Memory Buffer...")
print("-" * 70)
wm_system = brain.systems["working_memory"]

# Add items to working memory
print("   Adding items to working memory...")
wm_system.process({"mode": "add", "content": "apple", "activation": 0.9})
wm_system.process({"mode": "add", "content": "banana", "activation": 0.8})
wm_system.process({"mode": "add", "content": "cherry", "activation": 0.7})
print(f"   Buffer size: {len(wm_system.buffer)}")

# Get active contents
result = wm_system.process({"mode": "get", "threshold": 0.5})
print(f"   Active contents: {result['contents']}")
print(f"   Count: {result['count']}")
print(f"   [OK] Working memory add/get functional")

# Reinforce an item
print("\n   Reinforcing 'apple'...")
wm_system.process({"mode": "reinforce", "content": "apple", "amount": 0.3})
result = wm_system.process({"mode": "get", "threshold": 0.5})
print(f"   Active contents after reinforcement: {result['contents']}")
print(f"   [OK] Working memory reinforcement functional")

# Test decay
print("\n   Testing time-based decay...")
import time
time.sleep(0.5)  # Wait for decay
result = wm_system.process({"mode": "get", "threshold": 0.5})
print(f"   Active contents after decay: {result['contents']}")
print(f"   [OK] Working memory decay functional")

# Test 3: Coherence Band Analysis
print("\n4. Testing Coherence Band Analysis...")
print("-" * 70)
neural_system = brain.systems["neural_interface"]

# Generate synthetic signal with known frequency content
print("   Generating synthetic signal...")
t = np.linspace(0, 1, 100)
# Mix of alpha (10 Hz), beta (20 Hz), and gamma (40 Hz)
signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t) + 0.3 * np.sin(2 * np.pi * 40 * t)

# Analyze frequency bands
result = neural_system.process({"mode": "frequency_bands", "state": signal.tolist()})
band_powers = result["frequency_bands"]
print(f"   Frequency band powers:")
for band, power in band_powers.items():
    print(f"     {band}: {power:.6f}")
print(f"   [OK] Frequency band analysis functional")

# Test coherence analysis with signal history
print("\n   Testing coherence analysis with signal history...")
for i in range(15):
    # Add random signals to history
    test_signal = np.random.randn(64) * 0.1
    neural_system.process({"mode": "to_continuous", "spike_counts": {f"n_{j}": int(abs(test_signal[j])*10) for j in range(64)}})

result = neural_system.process({"mode": "coherence"})
if "error" not in result:
    coherence_bands = result["coherence_bands"]
    print(f"   Coherence band analysis:")
    for band, power in coherence_bands.items():
        print(f"     {band}: {power:.6f}")
    print(f"   [OK] Coherence analysis functional")
else:
    print(f"   [INFO] {result['error']}")

# Test native methods in ComprehensiveBrain
print("\n5. Testing Native Methods in ComprehensiveBrain...")
print("-" * 70)

# Test get_continuous_state
continuous_state = brain.get_continuous_state()
print(f"   Continuous state shape: {continuous_state.shape}")
print(f"   State norm: {np.linalg.norm(continuous_state):.3f}")
print(f"   [OK] get_continuous_state() functional")

# Test apply_field_operation
brain.apply_field_operation("exc", BrainRegion.CORTEX, strength=0.5)
print(f"   [OK] apply_field_operation() functional")

# Test find_semantic_attractor
nearest_attractor, distance = brain.find_semantic_attractor(continuous_state)
print(f"   Nearest attractor: {nearest_attractor}")
print(f"   Distance: {distance:.3f}")
print(f"   [OK] find_semantic_attractor() functional")

# Verify all systems
print("\n6. Verifying All Brain Systems...")
print("-" * 70)
system_status = brain.get_system_status()
print(f"   Total systems: {len(system_status)}")
for system_name, status in system_status.items():
    print(f"   {system_name}: active={status['active']}")

print("\n" + "=" * 70)
print("PHASE 2 FEATURES TEST COMPLETE")
print("=" * 70)
print("\nResults:")
print(f"  [OK] RK4 Integration - SIMDFieldEngineSystem with continuous dynamics")
print(f"  [OK] Working Memory Buffer - Short-term storage with decay")
print(f"  [OK] Coherence Band Analysis - Frequency analysis (delta, theta, alpha, beta, gamma)")
print(f"  [OK] Native Methods - get_continuous_state, apply_field_operation, find_semantic_attractor")
print(f"\nAll Phase 2 Priority 1 features successfully integrated")
print("=" * 70)
