import requests
import json

# Backend API URL
BASE_URL = "http://localhost:8000"

def demo_real_scraping():
    print("=== REAL MANUFACTURER DATA SCRAPING DEMO ===")
    print("This demonstrates how to scrape real data from manufacturer websites")
    print("like the Festo page you showed me with all technical specifications.")
    print()
    
    # Real Festo part from your example
    real_festo_part = {
        "manufacturer": "Festo",
        "part_id": "DSBC-63-400-PPVA-N3",
        "description": "ISO cylinder, double-acting, bore 63mm, stroke 400mm",
        "vendor": "Festo"
    }
    
    print("🎯 Target: Scraping real Festo part data")
    print(f"Part: {real_festo_part['manufacturer']} {real_festo_part['part_id']}")
    print(f"Description: {real_festo_part['description']}")
    print()
    
    # Test the scraping
    url = f"{BASE_URL}/scrape-parts"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "parts": [real_festo_part],
        "enrichment_prompt": "Extract technical specifications, pricing, and availability information"
    }
    
    try:
        print("🔄 Sending scraping request...")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        
        print("✅ Scraping completed!")
        print()
        
        # Show results
        result = data['results'][0]
        print(f"📊 Results for {result['manufacturer']} {result['part_id']}:")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print("✅ Part found and scraped successfully!")
            
            if 'extracted_info' in result['scraped_data']:
                info = result['scraped_data']['extracted_info']
                print("\n📋 Extracted Data:")
                print(f"  Title: {info.get('title', 'N/A')}")
                print(f"  Price: {info.get('price', 'N/A')}")
                print(f"  Availability: {info.get('availability', 'N/A')}")
                print(f"  Description: {info.get('description', 'N/A')}")
                print(f"  Part Number: {info.get('part_number', 'N/A')}")
                print(f"  Category: {info.get('category', 'N/A')}")
                print(f"  Material: {info.get('material', 'N/A')}")
                print(f"  Pressure: {info.get('pressure', 'N/A')}")
                print(f"  Temperature: {info.get('temperature', 'N/A')}")
                print(f"  Dimensions: {info.get('dimensions', 'N/A')}")
                print(f"  Weight: {info.get('weight', 'N/A')}")
                print(f"  Warranty: {info.get('warranty', 'N/A')}")
                print(f"  Specifications: {info.get('specifications', 'N/A')}")
            else:
                print("⚠️  No detailed data extracted (website structure may be complex)")
                
        elif result['status'] == 'not_found':
            print("❌ Part not found on manufacturer website")
            print("💡 This is common because:")
            print("   - Manufacturer websites often require authentication")
            print("   - Parts may be in different catalogs or regions")
            print("   - Website structure may have changed")
            print("   - Anti-bot measures may be blocking access")
            
        elif result['status'] == 'error':
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print()
        print("🔧 To get real data like the Festo page you showed:")
        print("1. Use the HTML test page: test_app.html")
        print("2. Try different part numbers")
        print("3. Check if the manufacturer website is accessible")
        print("4. Consider using manufacturer APIs if available")
        print()
        print("📈 The system is working - it's finding and attempting to scrape")
        print("   manufacturer websites, but real-world scraping requires:")
        print("   - Handling authentication")
        print("   - Bypassing anti-bot measures")
        print("   - Parsing complex website structures")
        print("   - Dealing with dynamic content")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing scraping: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    demo_real_scraping()
