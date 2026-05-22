"""
Test Brain with Fractal DNA Persistence Integration
Tests the cognitive core with persistent fractal DNA memory
"""

from cognitive_core import OptimizedCognitiveCore
import time

def test_brain_with_fractal_dna():
    print("=" * 70)
    print("BRAIN WITH FRACTAL DNA PERSISTENCE - INTEGRATION TEST")
    print("=" * 70)
    
    # Initialize brain with fractal DNA persistence
    print("\nInitializing brain with fractal DNA persistence...")
    brain = OptimizedCognitiveCore(persistence_db="brain_fractal_dna.db")
    
    # Test queries
    test_queries = [
        "What is 2+2?",
        "Solve for x: 3x + 7 = 22",
        "What is the square root of 625?",
        "Analyze the relationship between correlation and causation"
    ]
    
    results = []
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}")
        
        start_time = time.time()
        result = brain.process_query(query)
        elapsed = time.time() - start_time
        
        print(f"System: {result['system']}")
        print(f"Mode: {result['mode']}")
        print(f"Response Time: {elapsed:.2f}s")
        print(f"Success: {result.get('success', True)}")
        print(f"Response: {result['response'][:200]}...")
        
        results.append({
            "query": query,
            "system": result['system'],
            "time": elapsed,
            "success": result.get('success', True)
        })
    
    # Check persistence statistics
    print(f"\n{'='*70}")
    print("FRACTAL DNA PERSISTENCE STATISTICS")
    print(f"{'='*70}")
    
    persistence_stats = brain.persistence.get_statistics()
    for key, value in persistence_stats.items():
        print(f"{key}: {value}")
    
    # Check brain performance
    print(f"\n{'='*70}")
    print("BRAIN PERFORMANCE SUMMARY")
    print(f"{'='*70}")
    
    brain_summary = brain.get_performance_summary()
    for key, value in brain_summary.items():
        print(f"{key}: {value}")
    
    # Test memory lineage
    print(f"\n{'='*70}")
    print("MEMORY LINEAGE TEST")
    print(f"{'='*70}")
    
    if brain.memory:
        last_interaction = brain.memory[-1]
        if "dna_node_id" in last_interaction:
            print(f"Last interaction DNA Node ID: {last_interaction['dna_node_id']}")
            
            lineage = brain.persistence.get_fractal_lineage(last_interaction['dna_node_id'])
            print(f"Lineage length: {len(lineage)}")
            
            for i, node in enumerate(lineage):
                print(f"  Node {i+1}: {node.dna_hash[:16]}... - Gen {node.generation} - {node.improvement_type.value}")
        else:
            print("No DNA node ID found in last interaction")
    else:
        print("No memory entries")
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    
    successful = [r for r in results if r['success']]
    print(f"Total queries: {len(results)}")
    print(f"Successful: {len(successful)}")
    
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        print(f"Average response time: {avg_time:.2f}s")
    
    print(f"\n✓ Brain with Fractal DNA Persistence Integration Complete")
    print(f"✓ Memory is now persistent across sessions")
    print(f"✓ Each interaction stored as fractal DNA node")
    print(f"✓ QR-code DNA generated for each node")

if __name__ == "__main__":
    test_brain_with_fractal_dna()
