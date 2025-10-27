import requests
import json

# Backend API URL
BASE_URL = "http://localhost:8000"

def test_real_festo_scraping():
    print("--- Testing Real Festo Part Scraping ---")
    url = f"{BASE_URL}/scrape-parts"
    headers = {"Content-Type": "application/json"}

    # Real Festo part numbers for testing
    real_parts = [
        {
            "manufacturer": "Festo",
            "part_id": "DSBC-63-400-PPVA-N3",
            "description": "ISO cylinder, double-acting, bore 63mm, stroke 400mm",
            "vendor": "Festo"
        },
        {
            "manufacturer": "Festo", 
            "part_id": "B10099368",
            "description": "Pneumatic cylinder, double-acting, bore 32mm, stroke 100mm",
            "vendor": "Festo"
        },
        {
            "manufacturer": "SMC",
            "part_id": "CM2-32-100",
            "description": "Pneumatic cylinder, double-acting, bore 32mm, stroke 100mm",
            "vendor": "SMC"
        }
    ]

    payload = {
        "parts": real_parts,
        "enrichment_prompt": "Extract technical specifications, pricing, and availability information"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        print("Response Status Code:", response.status_code)
        print("Response Body:", json.dumps(data, indent=2))

        # Check results
        if data["success"]:
            print(f"\n✅ Scraping Results:")
            print(f"Total parts: {data['total_parts']}")
            print(f"Successful: {data['successful']}")
            print(f"Failed: {data['failed']}")
            print(f"Not found: {data['not_found']}")
            
            # Show detailed results
            for i, result in enumerate(data['results']):
                print(f"\n--- Part {i+1}: {result['manufacturer']} {result['part_id']} ---")
                print(f"Status: {result['status']}")
                
                if result['status'] == 'success' and 'extracted_info' in result['scraped_data']:
                    info = result['scraped_data']['extracted_info']
                    print(f"Title: {info.get('title', 'N/A')}")
                    print(f"Price: {info.get('price', 'N/A')}")
                    print(f"Availability: {info.get('availability', 'N/A')}")
                    print(f"Description: {info.get('description', 'N/A')}")
                    print(f"Part Number: {info.get('part_number', 'N/A')}")
                    print(f"Category: {info.get('category', 'N/A')}")
                    print(f"Material: {info.get('material', 'N/A')}")
                    print(f"Pressure: {info.get('pressure', 'N/A')}")
                    print(f"Temperature: {info.get('temperature', 'N/A')}")
                    print(f"Dimensions: {info.get('dimensions', 'N/A')}")
                    print(f"Weight: {info.get('weight', 'N/A')}")
                    print(f"Warranty: {info.get('warranty', 'N/A')}")
                elif result['status'] == 'not_found':
                    print("❌ Part not found on manufacturer website")
                elif result['status'] == 'error':
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print("❌ Scraping failed")

    except requests.exceptions.RequestException as e:
        print(f"Error testing real scraping: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Response content:", e.response.text)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_real_festo_scraping()
