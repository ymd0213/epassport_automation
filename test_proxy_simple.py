"""
Simple proxy test - minimal configuration
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import json
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

proxy_host = os.getenv('PROXY_HOST')
proxy_port = os.getenv('PROXY_PORT')
proxy_username = os.getenv('PROXY_USERNAME')
proxy_password = os.getenv('PROXY_PASSWORD')

print("="*70)
print("SIMPLE PROXY TEST")
print("="*70)
print(f"Proxy: {proxy_host}:{proxy_port}")
print(f"Username: {proxy_username}")
print("="*70)

# Create extension
extension_dir = tempfile.mkdtemp(prefix='proxy_simple_')

manifest = {
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Proxy Auth",
    "permissions": ["webRequest", "webRequestBlocking", "<all_urls>"],
    "background": {"scripts": ["background.js"], "persistent": True}
}

background_js = f"""
var credentials = {{username: "{proxy_username}", password: "{proxy_password}"}};
chrome.webRequest.onAuthRequired.addListener(
    function(details) {{
        console.log("AUTH REQUESTED:", details.url);
        return {{authCredentials: credentials}};
    }},
    {{urls: ["<all_urls>"]}},
    ['blocking']
);
console.log("PROXY AUTH LOADED");
"""

with open(os.path.join(extension_dir, 'manifest.json'), 'w') as f:
    json.dump(manifest, f)

with open(os.path.join(extension_dir, 'background.js'), 'w') as f:
    f.write(background_js)

print(f"Extension created: {extension_dir}")

# Setup Chrome options
options = Options()
options.add_argument(f"--proxy-server=http://{proxy_host}:{proxy_port}")
options.add_argument(f"--load-extension={extension_dir}")
options.add_argument("--disable-extensions-except=" + extension_dir)

print("Starting regular Chrome (not undetected)...")
driver = webdriver.Chrome(options=options)

print("✅ Chrome started! Waiting 5 seconds...")
time.sleep(5)

print("Navigating to ipify.org...")
driver.get("https://api.ipify.org?format=json")
time.sleep(5)

print("Page source:")
print(driver.page_source)

print("\nPress Enter to close...")
input()

driver.quit()

# Cleanup
import shutil
shutil.rmtree(extension_dir)
print("Done!")

