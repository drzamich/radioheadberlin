#!/usr/bin/env python3
import subprocess
import shlex

def check_page_for_date():
    """
    Reads curl command from file, executes it, and checks if '9. Dez' string is present.
    Returns True if found, False otherwise.
    """
    
    try:
        # Read the curl command from file
        with open('/Users/mdrzazga/Desktop/radiohead/curl_command.txt', 'r') as f:
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
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    result = check_page_for_date()
    print(result)
