# Proxy Quick Start Guide

## ✅ Your Configuration is Ready!

I detected your proxy configuration from the `.env` file:
```
PROXY_HOST=rp.scrapegw.com
PROXY_PORT=6060
PROXY_USERNAME=5e92mh4ca8b4j5b-country-us
PROXY_PASSWORD=bvfzhlfu3kmh8gr
```

## 🚀 How to Test

Run the test script to verify your proxy is working:

```bash
python test_proxy.py
```

The script will:
1. ✅ Load your proxy configuration
2. ✅ Start Chrome with proxy settings
3. ✅ Authenticate using Chrome DevTools Protocol (CDP)
4. ✅ Check your IP address (should show proxy IP, not your local IP)
5. ✅ Test navigation to the target website

## 🔧 How It Works

### Two-Step Proxy Configuration:

1. **Chrome Launch** - Browser starts with `--proxy-server` argument pointing to your proxy
2. **Authentication** - After browser starts, Chrome DevTools Protocol (CDP) injects authentication headers

### Why This Approach?

- ✅ Works reliably with `undetected_chromedriver`
- ✅ No temporary extensions needed
- ✅ Simple and clean implementation
- ✅ Supports both authenticated and non-authenticated proxies

## 📝 Environment Variables

Your `.env` file supports two formats:

### Format 1: Separate Variables (✅ Currently Using)
```bash
PROXY_HOST=rp.scrapegw.com
PROXY_PORT=6060
PROXY_USERNAME=5e92mh4ca8b4j5b-country-us
PROXY_PASSWORD=bvfzhlfu3kmh8gr
```

### Format 2: Single URL (Alternative)
```bash
PROXY_URL=http://username:password@host:port
```

Example:
```bash
PROXY_URL=http://5e92mh4ca8b4j5b-country-us:bvfzhlfu3kmh8gr@rp.scrapegw.com:6060
```

Both formats work! The code automatically detects which format you're using.

## 🔍 Expected Test Output

When you run `python test_proxy.py`, you should see:

```
======================================================================
PROXY CONFIGURATION TEST
======================================================================
📋 Loading proxy from separate variables

📋 Proxy Configuration:
   Host: rp.scrapegw.com
   Port: 6060
   Username: 5e92mh4ca8b4j5b-country-us
   Password: ************

🚀 Starting Chrome browser with proxy...
🔐 Configuring authenticated proxy: rp.scrapegw.com:6060
⏳ Initializing ChromeDriver...
✅ ChromeDriver initialized successfully
🔐 Setting up proxy authentication via Chrome DevTools Protocol...
✅ Proxy authentication configured via CDP

======================================================================
TEST 1: Checking IP address via ipify.org
======================================================================
✅ Your current IP address: XXX.XXX.XXX.XXX
   (This should be your proxy IP, not your local IP)

======================================================================
TEST 2: Checking IP address via icanhazip.com
======================================================================
✅ Your current IP address: XXX.XXX.XXX.XXX
   (This should be your proxy IP, not your local IP)

======================================================================
TEST 3: Navigating to target website
======================================================================
✅ Successfully loaded: U.S. Department of State - Online Passport Renewal
   URL: https://opr.travel.state.gov/

======================================================================
✅ PROXY TEST COMPLETED SUCCESSFULLY
======================================================================
```

## ⚠️ Troubleshooting

### Problem: Test shows my local IP instead of proxy IP

**Possible causes:**
1. Proxy credentials are incorrect
2. Proxy server is not reachable
3. Proxy server is blocking the connection

**Solutions:**
1. Verify credentials with your proxy provider (rp.scrapegw.com)
2. Test connectivity: `ping rp.scrapegw.com` or `telnet rp.scrapegw.com 6060`
3. Check if proxy service is active in your provider's dashboard

### Problem: Browser fails to start

**Possible causes:**
1. ChromeDriver version mismatch
2. Chrome browser not installed

**Solutions:**
1. The script auto-downloads the correct ChromeDriver version
2. Make sure Chrome browser is installed on your system

### Problem: CDP authentication fails

**Possible causes:**
1. Proxy server doesn't support HTTP Basic authentication
2. Special characters in password need encoding

**Solutions:**
1. Contact your proxy provider about authentication methods
2. Try the single URL format with URL-encoded password

## 🎯 Running the Main Script

Once the test is successful, run the main automation:

```bash
python main.py
```

The browser will restart between applications, applying fresh proxy settings each time.

## 📧 Support

If you encounter issues:
1. Run `python test_proxy.py` first
2. Check the error messages
3. Verify proxy credentials with your provider (rp.scrapegw.com)
4. Make sure the proxy service is active

