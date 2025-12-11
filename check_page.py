#!/usr/bin/env python3
import undetected_chromedriver as uc
import time
import os
from datetime import datetime

def play_sound():
    """Play system alert sound on macOS"""
    os.system('afplay /System/Library/Sounds/Basso.aiff')

def check_page_for_date(driver):
    """
    Uses Selenium to check if '12. Dez' string is present.
    Returns tuple: (success, found_date, has_radiohead, error_msg)
    """
    url = "https://www.fansale.de/tickets/all/radiohead/520"
    
    try:
        # Load the page
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page source
        page_source = driver.page_source
        
        # Check for the date and Radiohead
        found_date = "12. Dez" in page_source
        has_radiohead = "Radiohead" in page_source
        
        return (True, found_date, has_radiohead, None)
        
    except Exception as e:
        return (False, False, False, str(e))

if __name__ == "__main__":
    print("Starting monitoring with undetected Chrome... Press Ctrl+C to stop")
    print("Setting up Chrome driver...")
    print("-" * 60)
    
    # Create undetected Chrome driver
    options = uc.ChromeOptions()
    # options.add_argument('--headless=new')  # Uncomment to run in background
    
    driver = uc.Chrome(options=options)
    
    # Initial manual setup
    print("\n⏳ Opening page in browser...")
    print("Please manually solve any CAPTCHA or login if needed.")
    print("Once the page loads correctly, press ENTER to start monitoring...")
    
    url = "https://www.fansale.de/tickets/all/radiohead/520"
    driver.get(url)
    
    input("\nPress ENTER when page is ready: ")
    print("\n✓ Starting automated monitoring...")
    print("-" * 60)
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success, found_date, has_radiohead, error = check_page_for_date(driver)
            
            if not success:
                print(f"🔴 [{timestamp}] ERROR: Request failed - {error}")
                play_sound()
            elif not has_radiohead:
                print(f"⚠️  [{timestamp}] WARNING: Page doesn't contain 'Radiohead'")
                play_sound()
            elif found_date:
                print(f"✅ [{timestamp}] SUCCESS: Found '12. Dez' on page!")
            else:
                print(f"✓  [{timestamp}] OK: Radiohead present, but no '12. Dez' yet")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    finally:
        driver.quit()
        print("Browser closed.")
