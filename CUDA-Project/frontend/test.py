import requests
import json

def test_planner_endpoint():
    """Test the planner endpoint with an NLP prompt"""
    print("🧪 Testing Planner Endpoint...")
    
    url = "http://127.0.0.1:8000/planner"
    test_prompt = "Create a Python function that checks if a number is even or odd"
    
    payload = {"text": test_prompt}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received!")
            print(f"Keys in response: {list(data.keys())}")
            
            if "error" in data:
                print(f"❌ Error: {data['error']}")
                return False
            
            print(f"🏆 Winner: {data.get('winner', 'N/A')}")
            print(f"🧾 Reason: {data.get('reason', 'N/A')}")
            print(f"💻 Final Code: {data.get('final_code', 'N/A')[:100]}...")
            
            # Check if we have the expected fields
            if 'winner' in data and 'reason' in data and 'final_code' in data:
                print("✅ SUCCESS: Planner endpoint is working correctly!")
                return True
            else:
                print("❌ FAILED: Missing expected fields")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_run_agents_endpoint():
    """Test the run-agents endpoint with code input"""
    print("\n🧪 Testing Run-Agents Endpoint...")
    
    url = "http://127.0.0.1:8000/run-agents"
    test_code = "def divide(a, b): return a / b"
    
    payload = {"code": test_code}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received!")
            print(f"Keys in response: {list(data.keys())}")
            
            if "error" in data:
                print(f"❌ Error: {data['error']}")
                return False
            
            print(f"🏆 Winner: {data.get('winner', 'N/A')}")
            print(f"🧾 Reason: {data.get('reason', 'N/A')}")
            print(f"💻 Final Code: {data.get('final_code', 'N/A')[:100]}...")
            
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing CUDA API Endpoints...")
    
    # Test both endpoints
    planner_success = test_planner_endpoint()
    agents_success = test_run_agents_endpoint()
    
    if planner_success and agents_success:
        print("\n✅ All tests passed! The API is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the server and try again.") 