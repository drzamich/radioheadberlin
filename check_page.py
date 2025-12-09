#!/usr/bin/env python3
import subprocess

def check_page_for_date():
    """
    Fetches the page and checks if '9. Dez' string is present.
    Returns True if found, False otherwise.
    """
    url = "https://www.fansale.de/tickets/all/radiohead/520"
    
    try:
        # Use curl to fetch the page (force HTTP/1.1 to avoid stream issues)
        result = subprocess.run(
            ['curl', '-s', '-L', '--http1.1', '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Check if "9. Dez" is in the page content
            return "9. Dez" in result.stdout
        else:
            print(f"Error: curl failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
        
    except subprocess.TimeoutExpired:
        print("Error: Request timed out")
        return False
    except Exception as e:
        print(f"Error fetching page: {e}")
        return False

if __name__ == "__main__":
    result = check_page_for_date()
    print(result)
