#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    print("Starting monitoring with Selenium... Press Ctrl+C to stop")
    print("Setting up Chrome driver...")
    print("-" * 60)
    
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Create driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute script to hide automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })
    
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
