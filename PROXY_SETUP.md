# Proxy Configuration Guide

This guide explains how to configure and test proxy support in the automation script.

## Overview

The automation now supports both authenticated and non-authenticated proxies. The proxy configuration is loaded from environment variables and applied automatically when the browser starts.

## Features

✅ **Authenticated proxies** - Supports username/password authentication  
✅ **Non-authenticated proxies** - Simple proxy without credentials  
✅ **Multiple protocols** - HTTP, HTTPS, SOCKS5  
✅ **Browser restart** - Fresh browser instance with proxy for each application  
✅ **Automatic extension** - Chrome extension created automatically for authenticated proxies  

## Configuration

### Step 1: Add Proxy URL to .env File

Add the following line to your `.env` file:

#### For Authenticated Proxy (with username/password):
```bash
PROXY_URL=http://username:password@proxy-host:port
```

Example:
```bash
PROXY_URL=http://myuser:mypass@proxy.example.com:8080
```

#### For Non-Authenticated Proxy (no credentials):
```bash
PROXY_URL=http://proxy-host:port
```

Example:
```bash
PROXY_URL=http://proxy.example.com:8080
```

#### For SOCKS5 Proxy:
```bash
PROXY_URL=socks5://username:password@proxy-host:port
```

Example:
```bash
PROXY_URL=socks5://myuser:mypass@proxy.example.com:1080
```

### Step 2: Test Your Proxy Configuration

Before running the main automation, test your proxy configuration:

```bash
python test_proxy.py
```

This script will:
1. Load your proxy configuration from `.env`
2. Start Chrome with the proxy settings
3. Check your IP address via multiple services
4. Navigate to the target website
5. Display the results

**Expected Output:**
- Your IP address should be the proxy IP, not your local IP
- The browser should successfully load web pages through the proxy

## How It Works

### For Authenticated Proxies:
1. The script parses your proxy URL to extract host, port, username, and password
2. Creates a temporary Chrome extension that handles proxy authentication
3. Loads the extension into Chrome automatically
4. All traffic goes through the authenticated proxy

### For Non-Authenticated Proxies:
1. The script parses your proxy URL to extract host and port
2. Uses Chrome's `--proxy-server` argument
3. All traffic goes through the proxy

### Browser Restart Between Applications:
- After each application is processed, the browser is completely closed
- A fresh browser instance is created with the proxy settings
- This ensures clean state and proper proxy configuration for each application

## Troubleshooting

### Issue: Browser still shows local IP

**Possible Causes:**
1. Proxy URL format is incorrect in `.env` file
2. Proxy credentials are wrong
3. Proxy server is not reachable
4. Proxy server is blocking the connection

**Solutions:**
1. Verify the proxy URL format matches the examples above
2. Test the proxy with `test_proxy.py` script
3. Check proxy server status with your provider
4. Try a different proxy server

### Issue: Browser fails to start

**Possible Causes:**
1. Chrome extension creation failed (for authenticated proxies)
2. Invalid proxy URL format

**Solutions:**
1. Check the logs for error messages
2. Verify proxy URL in `.env` is correct
3. Try without authentication first to isolate the issue

### Issue: Websites don't load

**Possible Causes:**
1. Proxy server is blocking specific domains
2. Proxy server requires additional authentication
3. Network connectivity issues

**Solutions:**
1. Check with your proxy provider about domain restrictions
2. Verify credentials are correct
3. Test with `test_proxy.py` script first

## Advanced Configuration

### Using Different Proxies for Different Applications

If you need to rotate proxies, you can:
1. Create multiple `.env` files (e.g., `.env.proxy1`, `.env.proxy2`)
2. Switch between them by renaming before running the script
3. Or modify the script to load from different environment variables

### Proxy Rotation Service

If you're using a proxy rotation service that provides a single endpoint:
```bash
PROXY_URL=http://username:password@rotating-proxy.example.com:8080
```

The service will handle IP rotation automatically.

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit `.env` file** to version control
2. **Keep proxy credentials secure** - they have full access to your traffic
3. **Use HTTPS** when transmitting sensitive data
4. **Rotate credentials regularly** if using long-term proxies
5. **Temporary extension files** are automatically cleaned up after browser closes

## Verification Checklist

Before running the main automation, verify:

- [ ] Proxy URL is correctly formatted in `.env`
- [ ] `test_proxy.py` shows proxy IP (not local IP)
- [ ] Browser can load websites through proxy
- [ ] Target website (opr.travel.state.gov) is accessible
- [ ] Cloudflare captcha (if any) works with proxy

## Support

If you encounter issues:
1. Run `test_proxy.py` and check the output
2. Review the logs for error messages
3. Verify proxy configuration with your provider
4. Test with a simple non-authenticated proxy first

