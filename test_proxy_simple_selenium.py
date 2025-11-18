"""
Test proxy with regular Selenium (not undetected_chromedriver)
This helps isolate if the issue is with undetected_chromedriver
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from proxy_server import ProxyServer

print("="*70)
print("SIMPLE SELENIUM PROXY TEST")
print("="*70)

# Start local proxy server
print("\n1. Starting local proxy server...")
server = ProxyServer(local_host='127.0.0.1', local_port=8888)
server.start()
time.sleep(2)

# Setup Chrome with local proxy
print("\n2. Setting up Chrome with local proxy...")
options = Options()
options.add_argument("--proxy-server=http://127.0.0.1:8888")
options.add_argument("--start-maximized")

print("\n3. Starting Chrome (regular Selenium)...")
try:
    driver = webdriver.Chrome(options=options)
    print("✅ Chrome started successfully!")
    
    print("\n4. Testing proxy - checking IP address...")
    driver.get("https://api.ipify.org?format=json")
    time.sleep(5)
    
    print("\n5. Page content:")
    print(driver.page_source)
    
    print("\n6. Testing target website...")
    driver.get("https://opr.travel.state.gov/")
    time.sleep(5)
    
    print(f"\n✅ Successfully loaded: {driver.title}")
    print(f"   URL: {driver.current_url}")
    
    print("\n" + "="*70)
    print("✅ PROXY WORKS PERFECTLY!")
    print("="*70)
    print("\nBrowser will stay open for 20 seconds...")
    time.sleep(20)
    
    driver.quit()
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
finally:
    server.stop()
    print("Done!")

