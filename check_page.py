#!/usr/bin/env python3
import subprocess
import shlex
import time
from datetime import datetime

def check_page_for_date():
    """
    Reads curl command from file, executes it, and checks if '9. Dez' string is present.
    Returns tuple: (success, found_date, has_radiohead, response)
    """
    
    try:
        # Read the curl command from file
        with open('./curl_command.txt', 'r') as f:
            curl_command = f.read().strip()
        
        # Execute the curl command
        result = subprocess.run(
            curl_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            response = result.stdout
            found_date = "12. Dez" in response
            has_radiohead = "Radiohead" in response
            return (True, found_date, has_radiohead, response)
        else:
            return (False, False, False, f"curl failed with code {result.returncode}: {result.stderr}")
        
    except subprocess.TimeoutExpired:
        return (False, False, False, "Request timed out")
    except Exception as e:
        return (False, False, False, str(e))

if __name__ == "__main__":
    print("Starting monitoring... Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success, found_date, has_radiohead, response = check_page_for_date()
            
            if not success:
                print(f"🔴 [{timestamp}] ERROR: Request failed - {response}")
            elif not has_radiohead:
                print(f"⚠️  [{timestamp}] WARNING: Page doesn't contain 'Radiohead'")
            elif found_date:
                print(f"✅ [{timestamp}] SUCCESS: Found '12. Dez' on page!")
            else:
                print(f"✓  [{timestamp}] OK: Radiohead present, but no '12. Dez' yet")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
