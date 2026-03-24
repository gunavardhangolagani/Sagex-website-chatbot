# utils/updater.py
import os
import requests
from utils.web_crawler import fetch_wordpress_data
from utils.text_to_doc import process_all_documents
from utils.processing import fn_get_chroma_client

TARGET_WEBSITE_URL = "https://krytter.com/"
TIMESTAMP_FILE = "data/last_wp_update.txt"

# This tricks WordPress into thinking we are a normal Google Chrome browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_saved_timestamp():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            return f.read().strip()
    return None

def save_timestamp(timestamp):
    os.makedirs("data", exist_ok=True)
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(timestamp)

def background_refresh_knowledge_base():
    try:
        print("-> Fetching text from WordPress website...")
        raw_data = fetch_wordpress_data(TARGET_WEBSITE_URL)
        if not raw_data:
            print("-> ERROR: No data fetched.")
            return

        document_chunks = process_all_documents(raw_data)
        
        # 1. Get current store and delete
        vector_store = fn_get_chroma_client()
        try:
            vector_store.delete_collection()
            print("-> Old collection deleted.")
        except Exception as e:
            print(f"-> Note: Could not delete (might not exist): {e}")
        
        # 2. IMPORTANT: Force a fresh initialization of the collection
        print("-> Re-initializing and saving new data...")
        fresh_vector_store = fn_get_chroma_client(force_new=True)
        fresh_vector_store.add_documents(document_chunks)
        
        print(f"-> SUCCESS: Knowledge base refreshed with {len(document_chunks)} chunks!")
    except Exception as e:
        print(f"-> Refresh failed with error: {str(e)}")

def check_for_website_updates():
    print("\n--- Starting 15-Minute WordPress Check ---")
    last_known_time = get_saved_timestamp()
    print(f"-> Memory: Last known update was at {last_known_time}")
    
    try:
        api_url = f"{TARGET_WEBSITE_URL.rstrip('/')}/wp-json/wp/v2/pages?orderby=modified&order=desc&per_page=1"
        print(f"-> Asking WordPress API: {api_url}")
        
        # Added the HEADERS here to bypass security blockers!
        response = requests.get(api_url, headers=HEADERS, timeout=10) 
        print(f"-> WordPress responded with Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                latest_wp_date = data[0].get("modified")
                print(f"-> WordPress says newest page was edited at: {latest_wp_date}")
                
                if last_known_time is None or latest_wp_date > last_known_time:
                    print("-> CONCLUSION: Data is new! Triggering full web crawl...")
                    background_refresh_knowledge_base() 
                    save_timestamp(latest_wp_date)
                else:
                    print("-> CONCLUSION: Data is old. Skipping web crawl.")
            else:
                print("-> ERROR: WordPress returned 200, but the page list was empty.")
        else:
            print(f"-> ERROR: WordPress blocked us or failed. Response text: {response.text[:100]}")
                
    except Exception as e:
        print(f"-> ERROR: Checking WordPress failed completely: {str(e)}")
    print("------------------------------------------\n")