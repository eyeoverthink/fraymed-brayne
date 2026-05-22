"""
Test if the prompt wrapper is causing empty responses
"""

import requests

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma4"

def test_wrapper_prompt():
    print("Testing wrapper prompt...")
    
    query = "What is 2+2?"
    
    # This is what cognitive_core sends
    prompt = f"""You are a digital organism with fast, intuitive cognition.

User Query: {query}

Provide a direct, concise response. Be practical and to the point."""
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 50,
                "temperature": 0.7,
                "top_p": 0.9
            }
        },
        timeout=15
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        response_text = data.get("response", "")
        print(f"Response: '{response_text}'")
    else:
        print(f"Error: {response.text}")

def test_direct_prompt():
    print("\nTesting direct prompt...")
    
    query = "What is 2+2?"
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": query,
            "stream": False,
            "options": {
                "num_predict": 50,
                "temperature": 0.7,
                "top_p": 0.9
            }
        },
        timeout=15
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        response_text = data.get("response", "")
        print(f"Response: '{response_text}'")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_wrapper_prompt()
    test_direct_prompt()
