"""
Test the brain integration by simulating FraymusConvergence calls
This tests the HTTP bridge between Java and Python brain server
"""

import requests
import json
import time

BRAIN_SERVER_URL = "http://localhost:5000"

def test_health():
    """Test brain server health endpoint."""
    print("Testing brain server health...")
    try:
        response = requests.get(f"{BRAIN_SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_ask(query):
    """Test brain server ask endpoint."""
    print(f"\nTesting ask: '{query}'")
    start_time = time.time()
    
    try:
        payload = {"query": query}
        response = requests.post(
            f"{BRAIN_SERVER_URL}/ask",
            json=payload,
            timeout=15
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Response received in {elapsed:.2f}s")
            print(f"  System: {data.get('system')}")
            print(f"  Mode: {data.get('mode')}")
            print(f"  Response: {data.get('response', '')[:200]}...")
            print(f"  Success: {data.get('success')}")
            return True, elapsed
        else:
            print(f"✗ Ask failed: {response.status_code}")
            return False, elapsed
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"✗ Ask error: {e}")
        return False, elapsed

def test_stats():
    """Test brain server stats endpoint."""
    print("\nTesting brain server stats...")
    try:
        response = requests.get(f"{BRAIN_SERVER_URL}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Stats retrieved:")
            for key, value in data.items():
                print(f"  {key}: {value}")
            return True
        else:
            print(f"✗ Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Stats error: {e}")
        return False

def main():
    print("=" * 60)
    print("BRAIN INTEGRATION TEST")
    print("=" * 60)
    print("Simulating FraymusConvergence calls to brain server")
    
    # Test health
    if not test_health():
        print("\n❌ Brain server not available. Please start brain_server.py first.")
        return
    
    # Test various queries
    test_queries = [
        "What is 2+2?",
        "Solve for x: 3x + 7 = 22",
        "What is the square root of 625?",
        "If a train travels at 60 mph for 2.5 hours, how far does it travel?",
        "What is 15% of 480?",
        "Two cars approach each other from 100 miles apart. Car A travels at 60 mph, Car B at 40 mph. How long until they collide?",
        "Analyze the relationship between correlation and causation"
    ]
    
    results = []
    for query in test_queries:
        success, elapsed = test_ask(query)
        results.append({
            "query": query,
            "success": success,
            "time": elapsed
        })
    
    # Test stats
    test_stats()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"Total queries: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        avg_time = sum(r["time"] for r in successful) / len(successful)
        max_time = max(r["time"] for r in successful)
        min_time = min(r["time"] for r in successful)
        
        print(f"\nResponse time statistics:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        
        if avg_time < 10:
            print("\n✓ Response times acceptable for integration")
        else:
            print(f"\n⚠️ Response times may be slow (avg {avg_time:.2f}s)")
    
    print("\n" + "=" * 60)
    print("INTEGRATION STATUS")
    print("=" * 60)
    
    if len(successful) == len(results):
        print("✓ All tests passed - Brain integration working correctly")
        print("✓ Ready for FraymusConvergence integration")
    else:
        print(f"⚠️ {len(failed)} tests failed - Review errors above")
    
    print("\nNext steps:")
    print("1. Ensure brain_server.py is running (localhost:5000)")
    print("2. Compile FraymusConvergence.java")
    print("3. Run FraymusConvergence")
    print("4. Test 'ask' command in Fraymus")

if __name__ == "__main__":
    main()
