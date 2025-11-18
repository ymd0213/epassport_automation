"""
Test the local proxy server approach
"""

import undetected_chromedriver as uc
import time
from proxy_server import ProxyServer

print("="*70)
print("LOCAL PROXY SERVER TEST")
print("="*70)

# Start local proxy server
print("\n1. Starting local proxy server...")
server = ProxyServer(local_host='127.0.0.1', local_port=8888)
server.start()
time.sleep(2)

# Setup Chrome with local proxy
print("\n2. Setting up Chrome with local proxy (127.0.0.1:8888)...")
options = uc.ChromeOptions()
options.add_argument("--proxy-server=http://127.0.0.1:8888")
options.add_argument("--start-maximized")

print("\n3. Starting Chrome...")

# Try different ChromeDriver versions
driver = None
versions_to_try = [None, 142, 141, 140, 131, 130]

for version in versions_to_try:
    try:
        version_str = f"auto-detect" if version is None else f"version {version}"
        print(f"   Trying with {version_str}...")
        driver = uc.Chrome(options=options, version_main=version)
        print(f"✅ Chrome started successfully with {version_str}!")
        break
    except Exception as e:
        print(f"   Failed with {version_str}: {str(e)[:100]}")
        continue

if not driver:
    print("❌ Failed to start Chrome with any version")
    server.stop()
    exit(1)

print("\n4. Testing proxy - navigating to ipify.org...")
driver.get("https://api.ipify.org?format=json")
time.sleep(5)

print("\n5. Page content:")
print(driver.page_source)

print("\n6. Testing target website - navigating to opr.travel.state.gov...")
driver.get("https://opr.travel.state.gov/")
time.sleep(5)

print(f"\n✅ Successfully loaded: {driver.title}")
print(f"   URL: {driver.current_url}")

print("\n" + "="*70)
print("✅ TEST PASSED - No authentication popup!")
print("="*70)
print("\nBrowser will remain open for 30 seconds for inspection...")
print("Press Ctrl+C to close immediately.")

try:
    time.sleep(30)
except KeyboardInterrupt:
    print("\n\nTest interrupted by user")

# Cleanup
print("\nCleaning up...")
driver.quit()
server.stop()
print("Done!")

