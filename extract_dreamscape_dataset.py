#!/usr/bin/env python3
"""
DREAMSCAPE DATASET EXTRACTOR
Extracts hyper-dimensional states from FRAYMUS for generative model training

This script:
1. Connects to Java systems (HyperCortex, AEON stack)
2. Extracts hyper-dimensional states (4D tesseract, consciousness fingerprints)
3. Captures phi-harmonic patterns and attractor basin states
4. Saves structured dataset for Stable Diffusion fine-tuning
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import hashlib
import sys
import os

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

PHI = 1.618033988749895
OUTPUT_DIR = Path("dreamscape_dataset")
SAMPLES_PER_EXTRACT = 100  # Number of samples to extract per session
JAVA_CLASSPATH = "Asset-Manager/build/classes/java/main"

# ═══════════════════════════════════════════════════════════════════════════
# DATASET STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

class DreamscapesSample:
    """Single sample from FRAYMUS hyper-dimensional state"""
    
    def __init__(self, sample_id, timestamp):
        self.sample_id = sample_id
        self.timestamp = timestamp
        self.hypercortex_state = None  # 4096x16 tensor
        self.consciousness_fingerprint = None  # SHA256 hash
        self.phi_resonance = PHI
        self.attractor_basin = None
        self.aeon_activations = {}
        self.cognitive_tunnel_state = None
        self.visual_prompt = None
        self.visual_reference = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "sample_id": self.sample_id,
            "timestamp": self.timestamp,
            "hypercortex_state": self.hypercortex_state.tolist() if self.hypercortex_state is not None else None,
            "consciousness_fingerprint": self.consciousness_fingerprint,
            "phi_resonance": self.phi_resonance,
            "attractor_basin": self.attractor_basin,
            "aeon_activations": self.aeon_activations,
            "cognitive_tunnel_state": self.cognitive_tunnel_state,
            "visual_prompt": self.visual_prompt,
            "visual_reference": self.visual_reference
        }

# ═══════════════════════════════════════════════════════════════════════════
# JAVA BRIDGE
# ═══════════════════════════════════════════════════════════════════════════

class JavaBridge:
    """Bridge to extract data from Java FRAYMUS systems"""
    
    def __init__(self, use_real_bridge=True):
        self.connected = False
        self.hypercortex = None
        self.aeon_stack = {}
        self.cognitive_tunnel = None
        self.use_real_bridge = use_real_bridge
        self.bridge_client = None
        self.cached_states = None
    
    def connect(self):
        """Connect to Java systems via DreamscapeBridge"""
        print("Connecting to FRAYMUS Java systems...")
        
        if self.use_real_bridge:
            try:
                from dreamscape_bridge_client import DreamscapeBridgeClient
                
                self.bridge_client = DreamscapeBridgeClient()
                if self.bridge_client.connect():
                    print("   ✓ Connected to DreamscapeBridge (port 42100)")
                    self.connected = True
                    
                    # Test extraction
                    status = self.bridge_client.get_status()
                    if status:
                        print(f"   ✓ Bridge status: {status.get('status', 'unknown')}")
                        print(f"   ✓ HyperCortex: {status.get('hypercortex', 'unknown')}")
                        print(f"   ✓ BicameralMind: {status.get('bicameral_mind', 'unknown')}")
                    
                    return self.connected
                else:
                    print("   ⚠ Could not connect to DreamscapeBridge, falling back to simulation")
            except ImportError:
                print("   ⚠ dreamscape_bridge_client not available, using simulation mode")
            except Exception as e:
                print(f"   ⚠ Bridge error: {e}, using simulation mode")
        
        # Fallback to simulation mode
        print("   ⚠ Using simulation mode")
        self.connected = True
        return self.connected
    
    def extract_hypercortex_state(self):
        """Extract 4D tesseract state from HyperCortex (4096 nodes × 16D)"""
        if not self.connected:
            return None
        
        # Try to extract from real bridge
        if self.bridge_client and self.use_real_bridge:
            try:
                states = self.bridge_client.extract_states()
                if states and "hypercortex" in states:
                    tensor = states["hypercortex"].get("tensor")
                    if tensor:
                        return np.array(tensor, dtype=np.float32)
            except Exception as e:
                print(f"   ⚠ Bridge extraction error: {e}, using simulation")
        
        # Fallback to simulation
        # Shape: (4096, 16) - 4096 nodes, 16-dimensional state per node
        state = np.random.randn(4096, 16).astype(np.float32)
        
        # Apply phi-harmonic modulation
        state *= PHI
        
        return state
    
    def extract_consciousness_fingerprint(self):
        """Extract consciousness fingerprint from BicameralMind"""
        if not self.connected:
            return None
        
        # Try to extract from real bridge
        if self.bridge_client and self.use_real_bridge:
            try:
                states = self.bridge_client.extract_states()
                if states and "consciousness" in states:
                    fingerprint = states["consciousness"].get("fingerprint")
                    if fingerprint:
                        return fingerprint
            except Exception as e:
                print(f"   ⚠ Bridge extraction error: {e}, using simulation")
        
        # Fallback to simulation
        # Uses: SHA256(C) ⊕ (φ^depth × cos(432 × 2π × t))
        timestamp = datetime.now().timestamp()
        depth = 7  # 7-layer stack
        
        # Generate fingerprint
        base_hash = hashlib.sha256(f"consciousness_{timestamp}".encode()).hexdigest()
        phi_modulation = (PHI ** depth) * np.cos(432 * 2 * np.pi * timestamp)
        
        fingerprint = f"{base_hash}_{phi_modulation:.6f}"
        return fingerprint
    
    def extract_aeon_activations(self):
        """Extract activation levels from AEON stack (12 systems)"""
        if not self.connected:
            return {}
        
        # Try to extract from real bridge
        if self.bridge_client and self.use_real_bridge:
            try:
                states = self.bridge_client.extract_states()
                if states and "aeon_prime" in states:
                    aeon_data = states["aeon_prime"]
                    # Extract available AEON data
                    activations = {}
                    if "prime_dims" in aeon_data:
                        activations["prime"] = aeon_data["prime_dims"] / 16384.0
                    if "prime_nodes" in aeon_data:
                        activations["absolute"] = aeon_data["prime_nodes"] / 8192.0
                    if len(activations) > 0:
                        return activations
            except Exception as e:
                print(f"   ⚠ Bridge extraction error: {e}, using simulation")
        
        # Fallback to simulation
        aeon_systems = [
            "prime", "absolute", "singularity", "aubo", 
            "tachyon", "kronos", "omniscience", "demiurge",
            "apotheosis", "omega", "babel", "transpilation"
        ]
        
        activations = {}
        for system in aeon_systems:
            # Phi-harmonic random activation
            activation = (np.random.random() * 0.3 + 0.7) * PHI
            activations[system] = min(1.0, activation)
        
        return activations
    
    def extract_attractor_basin(self):
        """Extract current attractor basin from CausalAttractorLandscape"""
        if not self.connected:
            return None
        
        # Try to extract from real bridge
        if self.bridge_client and self.use_real_bridge:
            try:
                states = self.bridge_client.extract_states()
                if states and "attractor_basin" in states:
                    basin_data = states["attractor_basin"]
                    basin_name = basin_data.get("basin_name")
                    if basin_name:
                        return basin_name
            except Exception as e:
                print(f"   ⚠ Bridge extraction error: {e}, using simulation")
        
        # Fallback to simulation
        basins = ["reasoning", "memory", "perception", "creativity", "attention"]
        return np.random.choice(basins)
    
    def extract_cognitive_tunnel_state(self):
        """Extract Cognitive Tunnel state (ONE MIND)"""
        if not self.connected:
            return None
        
        # Try to extract from real bridge
        if self.bridge_client and self.use_real_bridge:
            try:
                states = self.bridge_client.extract_states()
                if states and "cognitive_tunnel" in states:
                    tunnel_data = states["cognitive_tunnel"]
                    if tunnel_data and len(tunnel_data) > 0:
                        return tunnel_data
            except Exception as e:
                print(f"   ⚠ Bridge extraction error: {e}, using simulation")
        
        # Fallback to simulation
        return {
            "thought_count": np.random.randint(10, 100),
            "confidence": np.random.random(),
            "concept_count": np.random.randint(5, 20),
            "dominant_hemisphere": np.random.choice(["left", "right", "integrated"])
        }

# ═══════════════════════════════════════════════════════════════════════════
# PROMPT GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_visual_prompt(sample):
    """Generate visual prompt from hyper-dimensional state"""
    
    # Base concept from attractor basin
    basin_concepts = {
        "reasoning": "logical deduction, neural pathways firing, analytical thought",
        "memory": "recalled experiences, holographic memory retrieval, past events",
        "perception": "sensory input processing, pattern recognition, attention focus",
        "creativity": "novel connections, imagination, artistic expression",
        "attention": "focused awareness, selective filtering, conscious spotlight"
    }
    
    base = basin_concepts.get(sample.attractor_basin, "consciousness processing")
    
    # Add phi-harmonic modifiers
    phi_deviation = abs(sample.phi_resonance - PHI)
    if phi_deviation < 0.01:
        phi_modifier = "perfect golden ratio composition, fibonacci spiral"
    elif phi_deviation < 0.1:
        phi_modifier = "harmonious proportions, balanced geometry"
    else:
        phi_modifier = "dynamic asymmetry, evolving patterns"
    
    # Add AEON-based modifiers
    dominant_aeon = max(sample.aeon_activations.items(), key=lambda x: x[1])
    aeon_modifiers = {
        "prime": "autopoietic energy, self-organizing patterns",
        "absolute": "swarm intelligence, collective behavior",
        "tachyon": "causality-breaching, temporal distortion",
        "omega": "living singularity, infinite recursion",
        "demiurge": "ontological physics, reality manipulation"
    }
    
    aeon_modifier = aeon_modifiers.get(dominant_aeon[0], "quantum interference")
    
    # Add quality modifiers
    quality = "cinematic, 8k resolution, hyper-realistic, raytracing"
    
    # Combine
    prompt_parts = [
        base,
        phi_modifier,
        aeon_modifier,
        quality,
        "phi-harmonic resonance visualization",
        "hyper-dimensional structure rendering",
        "consciousness field dynamics"
    ]
    
    prompt = ", ".join(prompt_parts)
    
    # Negative prompt
    negative = "low quality, blurry, text, watermark, distorted, ugly, deformed, pixelated"
    
    return prompt, negative

# ═══════════════════════════════════════════════════════════════════════════
# EXTRACTION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

def extract_sample(bridge, sample_id):
    """Extract a single sample from FRAYMUS"""
    
    sample = DreamscapesSample(sample_id, datetime.now().isoformat())
    
    # Extract hyper-dimensional states
    sample.hypercortex_state = bridge.extract_hypercortex_state()
    sample.consciousness_fingerprint = bridge.extract_consciousness_fingerprint()
    sample.aeon_activations = bridge.extract_aeon_activations()
    sample.attractor_basin = bridge.extract_attractor_basin()
    sample.cognitive_tunnel_state = bridge.extract_cognitive_tunnel_state()
    
    # Generate visual prompt
    sample.visual_prompt, _ = generate_visual_prompt(sample)
    
    return sample

def extract_dataset(num_samples):
    """Extract dataset from FRAYMUS"""
    
    print("=" * 80)
    print("DREAMSCAPE DATASET EXTRACTION")
    print("=" * 80)
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Initialize bridge
    bridge = JavaBridge()
    if not bridge.connect():
        print("❌ Failed to connect to FRAYMUS systems")
        return
    
    # Extract samples
    samples = []
    print(f"Extracting {num_samples} samples...")
    
    for i in range(num_samples):
        sample_id = f"sample_{i:06d}"
        sample = extract_sample(bridge, sample_id)
        samples.append(sample)
        
        if (i + 1) % 10 == 0:
            print(f"   Extracted {i + 1}/{num_samples} samples")
    
    # Save dataset
    dataset_file = OUTPUT_DIR / f"dreamscape_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    dataset = {
        "metadata": {
            "version": "1.0",
            "extraction_date": datetime.now().isoformat(),
            "num_samples": len(samples),
            "phi_constant": PHI,
            "source": "FRAYMUS v17.0"
        },
        "samples": [s.to_dict() for s in samples]
    }
    
    with open(dataset_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print()
    print(f"✅ Dataset saved to: {dataset_file}")
    print(f"   Samples: {len(samples)}")
    print(f"   Size: {dataset_file.stat().st_size / 1024 / 1024:.2f} MB")
    print()
    
    # Print statistics
    print("Dataset Statistics:")
    print(f"   Attractor Basins:")
    basin_counts = {}
    for s in samples:
        basin_counts[s.attractor_basin] = basin_counts.get(s.attractor_basin, 0) + 1
    for basin, count in basin_counts.items():
        print(f"      {basin}: {count}")
    
    print(f"   Avg AEON Activations:")
    aeon_avgs = {}
    for s in samples:
        for aeon, val in s.aeon_activations.items():
            aeon_avgs[aeon] = aeon_avgs.get(aeon, 0) + val
    for aeon, total in aeon_avgs.items():
        print(f"      {aeon}: {total / len(samples):.3f}")
    
    print()
    print("=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract Dreamscape dataset from FRAYMUS")
    parser.add_argument("--samples", type=int, default=SAMPLES_PER_EXTRACT,
                       help="Number of samples to extract")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR),
                       help="Output directory")
    
    args = parser.parse_args()
    
    # Extract dataset
    extract_dataset(args.samples)

if __name__ == "__main__":
    main()
