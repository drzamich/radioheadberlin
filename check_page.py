#!/usr/bin/env python3
import urllib.request
import ssl
from bs4 import BeautifulSoup

def check_page_for_date():
    """
    Fetches the page and checks if '9. Dez' string is present.
    Returns True if found, False otherwise.
    """
    url = "https://www.fansale.de/tickets/all/radiohead/520"
    
    try:
        # Create SSL context that doesn't verify certificates (for testing)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # Fetch the page with browser-like headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # Parse the content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check if "9. Dez" is in the page text
        page_text = soup.get_text()
        result = "9. Dez" in page_text
        
        return result
        
    except Exception as e:
        print(f"Error fetching page: {e}")
        return False

if __name__ == "__main__":
    result = check_page_for_date()
    print(result)
