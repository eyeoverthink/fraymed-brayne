"""
Demonstrate Digital Organism Brain Capabilities
Shows what the brain can do across different domains
"""

from cognitive_core import OptimizedCognitiveCore
import time

def demonstrate_capabilities():
    print("=" * 70)
    print("DIGITAL ORGANISM BRAIN - CAPABILITY DEMONSTRATION")
    print("=" * 70)
    
    brain = OptimizedCognitiveCore()
    
    demonstrations = [
        ("Math Calculation", "What is 247 * 389?"),
        ("Algebra", "Solve for x: 3x + 7 = 22"),
        ("Physics", "Two cars approach from 100 miles apart. Car A at 60 mph, Car B at 40 mph. How long until collision?"),
        ("Data Analysis", "What is 15% of 480?"),
        ("Word Problem", "If a train travels at 60 mph for 2.5 hours, how far does it travel?"),
        ("Complex Reasoning", "Analyze the relationship between correlation and causation"),
        ("Pattern Recognition", "What is the square root of 625?"),
        ("Creative Thinking", "Explain the concept of entropy in simple terms"),
    ]
    
    results = []
    
    for category, query in demonstrations:
        print(f"\n{'='*70}")
        print(f"DEMONSTRATION: {category}")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print("-" * 70)
        
        start_time = time.time()
        result = brain.process_query(query)
        elapsed = time.time() - start_time
        
        print(f"System: {result['system']}")
        print(f"Mode: {result['mode']}")
        print(f"Response Time: {elapsed:.2f}s")
        print(f"Success: {result.get('success', True)}")
        print(f"\nResponse:")
        print(result['response'])
        
        results.append({
            "category": category,
            "query": query,
            "system": result['system'],
            "time": elapsed,
            "success": result.get('success', True)
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("DEMONSTRATION SUMMARY")
    print(f"{'='*70}")
    
    successful = [r for r in results if r['success']]
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        print(f"Total demonstrations: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Average response time: {avg_time:.2f}s")
        
        system_1_count = sum(1 for r in successful if r['system'] == 'System 1')
        system_2_count = sum(1 for r in successful if r['system'] == 'System 2')
        print(f"System 1 (fast/intuitive): {system_1_count}")
        print(f"System 2 (deep/analytical): {system_2_count}")
    
    # Performance summary
    print(f"\n{'='*70}")
    print("BRAIN PERFORMANCE SUMMARY")
    print(f"{'='*70}")
    summary = brain.get_performance_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    demonstrate_capabilities()
