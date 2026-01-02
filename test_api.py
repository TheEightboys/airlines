import urllib.request
import json

def test_api(endpoint):
    try:
        url = f"http://localhost:5000{endpoint}"
        print(f"\nTesting: {url}")
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"Status: {response.status}")
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
    except Exception as e:
        print(f"Error: {e}")

# Test destinations API
test_api("/api/destinations")

# Test recommendations for our three countries
for country in ["UZBEKISTAN", "MALTA", "ARMENIA"]:
    test_api(f"/api/recommend/{country}")