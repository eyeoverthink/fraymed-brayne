"""
Test Ollama API directly to diagnose performance issues
"""

import requests
import time

OLLAMA_BASE_URL = "http://localhost:11434"

def test_ollama_connection():
    """Test if Ollama is running."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama is running")
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            print(f"  Available models: {models}")
            return True
        else:
            print(f"✗ Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama: {e}")
        return False

def test_model_response(model, prompt, timeout):
    """Test a specific model's response time."""
    print(f"\nTesting {model} with timeout {timeout}s...")
    print(f"Prompt: {prompt}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 50,
                    "temperature": 0.7
                }
            },
            timeout=timeout
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "")
            print(f"✓ Response received in {elapsed:.2f}s")
            print(f"  Response: {response_text[:100]}...")
            return elapsed, response_text
        else:
            print(f"✗ Error: {response.status_code}")
            return elapsed, None
    
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"✗ Timeout after {elapsed:.2f}s")
        return elapsed, None
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"✗ Error: {e}")
        return elapsed, None

def main():
    print("=" * 60)
    print("Ollama API Direct Test")
    print("=" * 60)
    
    # Test connection
    if not test_ollama_connection():
        print("\nOllama is not running. Please start Ollama first.")
        return
    
    # Test different models with different timeouts
    test_cases = [
        ("gemma4", "What is 2+2?", 5),
        ("gemma4", "What is 2+2?", 10),
        ("gemma4", "What is 2+2?", 30),
        ("deepseek-r1", "What is 2+2?", 10),
        ("deepseek-r1", "What is 2+2?", 30),
    ]
    
    results = []
    
    for model, prompt, timeout in test_cases:
        elapsed, response = test_model_response(model, prompt, timeout)
        results.append({
            "model": model,
            "timeout": timeout,
            "elapsed": elapsed,
            "success": response is not None
        })
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for result in results:
        status = "✓" if result["success"] else "✗"
        print(f"{status} {result['model']} (timeout {result['timeout']}s): {result['elapsed']:.2f}s")
    
    # Analysis
    successful = [r for r in results if r["success"]]
    if successful:
        avg_time = sum(r["elapsed"] for r in successful) / len(successful)
        print(f"\nAverage response time for successful requests: {avg_time:.2f}s")
        
        if avg_time < 5:
            print("Response times are acceptable")
        elif avg_time < 10:
            print("Response times are moderate")
        else:
            print("Response times are too slow - need optimization")
    else:
        print("\n⚠️ All requests failed - Ollama may not be responding properly")

if __name__ == "__main__":
    main()
