#!/usr/bin/env python3
"""
Test script for the Web Scraping & AI Enrichment API
This script helps debug why data is not being retrieved.
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_part_scraping():
    """Test the part scraping endpoint"""
    try:
        # Sample part data
        test_data = {
            "parts": [
                {
                    "manufacturer": "Festo",
                    "part_id": "B10099368",
                    "description": "Pneumatic cylinder, double-acting, bore 32mm, stroke 100mm",
                    "vendor": None
                }
            ],
            "enrichment_prompt": "Extract technical specifications and pricing information"
        }
        
        print("🔄 Testing part scraping...")
        response = requests.post(
            f"{API_BASE_URL}/scrape-parts",
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Part Scraping Successful!")
            print(f"Results: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Part Scraping Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Part Scraping Error: {e}")
        return False

def test_regular_scraping():
    """Test the regular URL scraping endpoint"""
    try:
        test_data = {
            "urls": ["https://httpbin.org/html"],
            "selectors": {
                "title": "h1",
                "content": "p"
            }
        }
        
        print("🔄 Testing regular URL scraping...")
        response = requests.post(
            f"{API_BASE_URL}/scrape",
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Regular Scraping Successful!")
            print(f"Results: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Regular Scraping Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Regular Scraping Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing API Health...")
    if not test_health():
        print("❌ API is not running. Please start the backend with: python main.py")
        return
    
    # Test 2: Regular Scraping
    print("\n2. Testing Regular URL Scraping...")
    test_regular_scraping()
    
    # Test 3: Part Scraping
    print("\n3. Testing Part Scraping...")
    test_part_scraping()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main()
