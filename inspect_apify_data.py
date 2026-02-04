import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def inspect_dataset(run_id="GSoMMJh0hb6PZ1e9u"):
    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
    print(f"🧐 Inspeccionando Dataset del Run: {run_id}")
    try:
        run = client.run(run_id).get()
        dataset_id = run['defaultDatasetId']
        items = client.dataset(dataset_id).list_items(limit=3).items
        for i, item in enumerate(items):
            print(f"\n--- Item {i+1} ---")
            print(item.keys())
            # Print a few key values to identify names
            for key in ['title', 'name', 'placeName', 'authorName', 'text', 'rating', 'stars']:
                if key in item:
                    print(f"{key}: {item[key]}")
    except Exception as e:
        print(f"❌ Error inspeccionando dataset: {e}")

if __name__ == "__main__":
    inspect_dataset()
