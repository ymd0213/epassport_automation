"""
Test script to verify proxy configuration is working correctly
"""

import undetected_chromedriver as uc
import os
import time
import json
import tempfile
from urllib.parse import urlparse
from dotenv import load_dotenv

def create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    """Create a Chrome extension for proxy authentication"""
    try:
        if not proxy_username or not proxy_password:
            return None
        
        # Create a temporary directory for the extension files
        extension_dir = tempfile.mkdtemp(prefix='proxy_ext_test_')
        
        # Create manifest.json
        manifest_json = {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy Auth",
            "permissions": [
                "webRequest",
                "webRequestBlocking",
                "<all_urls>",
                "proxy",
                "tabs",
                "storage"
            ],
            "background": {
                "scripts": ["background.js"],
                "persistent": True
            },
            "minimum_chrome_version": "22.0.0"
        }
        
        # Escape special characters in credentials
        username = proxy_username.replace('\\', '\\\\').replace('"', '\\"')
        password = proxy_password.replace('\\', '\\\\').replace('"', '\\"')
        
        # Create background.js with proxy authentication
        background_js = f"""
// Proxy authentication extension
console.log('='.repeat(50));
console.log('Proxy Auth Extension Starting...');
console.log('Target: {proxy_host}:{proxy_port}');
console.log('Username: {username}');
console.log('='.repeat(50));

// Authentication credentials
var credentials = {{
    username: "{username}",
    password: "{password}"
}};

// Handle authentication requests
function handleAuthRequest(details) {{
    console.log('🔐 Authentication requested!');
    console.log('   URL:', details.url);
    console.log('   Challenger:', details.challenger);
    console.log('   isProxy:', details.isProxy);
    console.log('   Providing credentials...');
    
    return {{
        authCredentials: credentials
    }};
}}

// Register the authentication handler
chrome.webRequest.onAuthRequired.addListener(
    handleAuthRequest,
    {{urls: ["<all_urls>"]}},
    ['blocking']
);

console.log('✅ Proxy authentication handler registered');
console.log('   Listening for auth requests on all URLs');
console.log('='.repeat(50));
"""
        
        # Write manifest.json
        manifest_path = os.path.join(extension_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_json, f, indent=2)
        
        # Write background.js
        background_path = os.path.join(extension_dir, 'background.js')
        with open(background_path, 'w', encoding='utf-8') as f:
            f.write(background_js)
        
        print(f"✅ Proxy authentication extension created at: {extension_dir}")
        return extension_dir
        
    except Exception as e:
        print(f"❌ Error creating proxy extension: {str(e)}")
        return None

def test_proxy():
    """Test proxy configuration by checking IP address"""
    print("="*70)
    print("PROXY CONFIGURATION TEST")
    print("="*70)
    
    # Load environment variables
    load_dotenv()
    
    # Method 1: Try to get proxy URL from single environment variable
    proxy_url = os.getenv('PROXY_URL')
    
    if proxy_url:
        # Parse the proxy URL
        parsed = urlparse(proxy_url)
        proxy_host = parsed.hostname
        proxy_port = parsed.port
        proxy_username = parsed.username
        proxy_password = parsed.password
        print("📋 Loading proxy from PROXY_URL")
    else:
        # Method 2: Try to get proxy configuration from separate variables
        proxy_host = os.getenv('PROXY_HOST')
        proxy_port = os.getenv('PROXY_PORT')
        proxy_username = os.getenv('PROXY_USERNAME')
        proxy_password = os.getenv('PROXY_PASSWORD')
        
        if not proxy_host or not proxy_port:
            print("❌ No proxy configuration found in .env file")
            print("\nPlease add proxy configuration to your .env file:")
            print("\nOption 1 - Single URL:")
            print("  PROXY_URL=http://username:password@proxy-host:port")
            print("\nOption 2 - Separate variables:")
            print("  PROXY_HOST=proxy-host")
            print("  PROXY_PORT=port")
            print("  PROXY_USERNAME=username")
            print("  PROXY_PASSWORD=password")
            return
        
        # Convert port to integer
        try:
            proxy_port = int(proxy_port)
        except ValueError:
            print(f"❌ Invalid PROXY_PORT value: {proxy_port}")
            return
        
        # Build proxy_url for compatibility
        scheme = 'http'  # Default to http
        if proxy_username and proxy_password:
            proxy_url = f"{scheme}://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
        else:
            proxy_url = f"{scheme}://{proxy_host}:{proxy_port}"
        
        print("📋 Loading proxy from separate variables")
    
    print(f"\n📋 Proxy Configuration:")
    print(f"   Host: {proxy_host}")
    print(f"   Port: {proxy_port}")
    if proxy_username:
        print(f"   Username: {proxy_username}")
        print(f"   Password: {'*' * len(proxy_password) if proxy_password else 'None'}")
    else:
        print(f"   Authentication: None")
    
    print("\n🚀 Starting Chrome browser with proxy...")
    
    driver = None
    proxy_extension_path = None
    
    try:
        # Create Chrome options
        options = uc.ChromeOptions()
        
        # ALWAYS set proxy-server argument (for both authenticated and non-authenticated)
        proxy_server = f"http://{proxy_host}:{proxy_port}"
        options.add_argument(f"--proxy-server={proxy_server}")
        print(f"🌐 Proxy server configured: {proxy_server}")
        
        # If authenticated, also load extension for automatic credential handling
        if proxy_username and proxy_password:
            print(f"🔐 Setting up proxy authentication extension...")
            proxy_extension_path = create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password)
            
            if proxy_extension_path:
                # Load the extension
                options.add_argument(f'--load-extension={proxy_extension_path}')
                print(f"✅ Proxy extension loaded from: {proxy_extension_path}")
            else:
                print("❌ Failed to create proxy extension - authentication may fail")
                return
        else:
            print(f"ℹ️  Non-authenticated proxy (no credentials needed)")
        
        # Additional options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Enable extension loading (important for proxy auth extension)
        if proxy_extension_path:
            options.add_argument("--disable-extensions-except=" + proxy_extension_path)
            options.add_argument("--disable-extensions-file-access-check")
        
        # Create driver
        print("⏳ Initializing ChromeDriver with version 142...")
        driver = uc.Chrome(options=options, version_main=142)
        print("✅ ChromeDriver initialized successfully")
        
        # Wait a moment for the extension to initialize
        if proxy_username and proxy_password:
            print("⏳ Waiting 5 seconds for proxy extension to initialize...")
            time.sleep(5)
        
        # Test 1: Check IP address via ipify.org
        print("\n" + "="*70)
        print("TEST 1: Checking IP address via ipify.org")
        print("="*70)
        
        driver.get("https://api.ipify.org?format=json")
        time.sleep(3)
        
        try:
            page_source = driver.page_source
            # Extract IP from JSON response
            if '"ip"' in page_source:
                import re
                ip_match = re.search(r'"ip":"([\d\.]+)"', page_source)
                if ip_match:
                    detected_ip = ip_match.group(1)
                    print(f"✅ Your current IP address: {detected_ip}")
                    print(f"   (This should be your proxy IP, not your local IP)")
        except Exception as e:
            print(f"⚠️  Could not parse IP address: {str(e)}")
        
        # Test 2: Check IP via icanhazip.com
        print("\n" + "="*70)
        print("TEST 2: Checking IP address via icanhazip.com")
        print("="*70)
        
        driver.get("https://icanhazip.com")
        time.sleep(3)
        
        try:
            page_source = driver.page_source
            # Extract IP from plain text response
            import re
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', page_source)
            if ip_match:
                detected_ip = ip_match.group(1)
                print(f"✅ Your current IP address: {detected_ip}")
                print(f"   (This should be your proxy IP, not your local IP)")
        except Exception as e:
            print(f"⚠️  Could not parse IP address: {str(e)}")
        
        # Test 3: Navigate to target website
        print("\n" + "="*70)
        print("TEST 3: Navigating to target website")
        print("="*70)
        
        driver.get("https://opr.travel.state.gov/")
        time.sleep(5)
        
        print(f"✅ Successfully loaded: {driver.title}")
        print(f"   URL: {driver.current_url}")
        
        print("\n" + "="*70)
        print("✅ PROXY TEST COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\n⚠️  Browser will remain open for 30 seconds for manual inspection.")
        print("   Please verify that the IP address shown is your proxy IP.")
        print("   Press Ctrl+C to close immediately.")
        
        # Keep browser open for inspection
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during proxy test: {str(e)}")
        print(f"   This could indicate:")
        print(f"   1. Proxy credentials are incorrect")
        print(f"   2. Proxy server is not reachable")
        print(f"   3. Proxy server is down or blocking connections")
    finally:
        # Close driver
        if driver:
            try:
                driver.quit()
                print("\n✅ Browser closed")
            except:
                pass
        
        # Clean up proxy extension
        if proxy_extension_path and os.path.exists(proxy_extension_path):
            try:
                import shutil
                shutil.rmtree(proxy_extension_path)
                print("✅ Proxy extension cleaned up")
            except Exception as e:
                print(f"⚠️  Failed to clean up proxy extension: {str(e)}")

if __name__ == "__main__":
    test_proxy()

