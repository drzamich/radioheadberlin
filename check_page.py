#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def check_page_for_date():
    """
    Fetches the page and checks if '9. Dez' string is present.
    Returns True if found, False otherwise.
    """
    url = "https://www.fansale.de/tickets/all/radiohead/520"
    
    try:
        # Fetch the page with browser-like headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if "9. Dez" is in the page text
        page_text = soup.get_text()
        result = "9. Dez" in page_text
        
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return False

if __name__ == "__main__":
    result = check_page_for_date()
    print(result)
