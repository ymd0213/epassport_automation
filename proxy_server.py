"""
Local HTTP proxy server that handles authentication to upstream proxy
This acts as a bridge between Chrome and the authenticated proxy
"""

import socket
import threading
import base64
import select
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

class ProxyServer:
    def __init__(self, local_host='127.0.0.1', local_port=8888):
        self.local_host = local_host
        self.local_port = local_port
        self.running = False
        self.server_socket = None
        
        # Load proxy credentials from environment
        load_dotenv()
        self.proxy_host = os.getenv('PROXY_HOST')
        self.proxy_port = int(os.getenv('PROXY_PORT'))
        self.proxy_username = os.getenv('PROXY_USERNAME')
        self.proxy_password = os.getenv('PROXY_PASSWORD')
        
        # Load target domain (government site) from environment
        # Only this domain will be routed through the residential proxy
        self.target_domain = os.getenv('TARGET_DOMAIN', 'opr.travel.state.gov')
        
        # Proxy mode control
        # "proxy" = route target domain through residential proxy (for captcha)
        # "direct" = bypass proxy for all domains (after captcha passed)
        self.mode_lock = threading.Lock()
        self._proxy_enabled = True  # Start with proxy enabled for captcha
        
        # Statistics tracking
        self.stats_lock = threading.Lock()
        self.proxied_count = 0
        self.bypassed_count = 0
        
        # Create auth header
        credentials = f"{self.proxy_username}:{self.proxy_password}"
        self.auth_header = f"Proxy-Authorization: Basic {base64.b64encode(credentials.encode()).decode()}\r\n"
        
    
    def start(self):
        """Start the proxy server in a background thread"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.local_host, self.local_port))
        self.server_socket.listen(50)
        
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        
    
    def stop(self):
        """Stop the proxy server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
    
    def get_stats(self):
        """Get current statistics"""
        with self.stats_lock:
            return {
                'proxied': self.proxied_count,
                'bypassed': self.bypassed_count,
                'total': self.proxied_count + self.bypassed_count
            }
    
    def enable_proxy(self):
        """Enable proxy mode - route target domain through residential proxy"""
        with self.mode_lock:
            self._proxy_enabled = True
    
    def disable_proxy(self):
        """Disable proxy mode - all connections go direct (bypass proxy)"""
        with self.mode_lock:
            self._proxy_enabled = False
    
    def is_proxy_enabled(self):
        """Check if proxy mode is enabled"""
        with self.mode_lock:
            return self._proxy_enabled
    
    def _run(self):
        """Main server loop"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                thread.start()
            except:
                break
    
    def _should_use_proxy(self, host):
        """
        Determine if the target host should be routed through the residential proxy
        
        Args:
            host (str): Target hostname (e.g., "opr.travel.state.gov:443")
            
        Returns:
            bool: True if should use proxy, False if should bypass (direct connection)
        """
        # Check if proxy mode is enabled
        with self.mode_lock:
            if not self._proxy_enabled:
                return False  # Proxy disabled, all connections go direct
        
        # Extract hostname without port
        hostname = host.split(':')[0].lower()
        
        # Cloudflare-related domains to route through proxy
        cloudflare_domains = [
            'cloudflare.com',
            'challenges.cloudflare.com',
            'cloudflareinsights.com',
            'cloudflare-dns.com',
            'cloudflareclient.com',
            'cloudflarestream.com',
            'cloudflaressl.com',
        ]
        
        # Check if hostname matches any Cloudflare domain
        for cf_domain in cloudflare_domains:
            if hostname == cf_domain or hostname.endswith('.' + cf_domain):
                return True
        
        return False
    
    def _handle_client(self, client_socket):
        """Handle a client connection"""
        try:
            # Read request from client
            request = b""
            while True:
                chunk = client_socket.recv(4096)
                request += chunk
                if len(chunk) < 4096 or b"\r\n\r\n" in request:
                    break
            
            if not request:
                client_socket.close()
                return
            
            # Parse the request
            request_str = request.decode('utf-8', errors='ignore')
            lines = request_str.split('\r\n')
            
            # Check if it's a CONNECT request (for HTTPS)
            if lines[0].startswith('CONNECT'):
                self._handle_connect(client_socket, request_str)
            else:
                self._handle_http(client_socket, request)
                
        except Exception:
            pass
        finally:
            client_socket.close()
    
    def _handle_connect(self, client_socket, request_str):
        """Handle HTTPS CONNECT request"""
        try:
            # Extract target host and port
            lines = request_str.split('\r\n')
            target = lines[0].split(' ')[1]
            
            # Check if this domain should use the proxy
            if self._should_use_proxy(target):
                # Route through residential proxy
                with self.stats_lock:
                    self.proxied_count += 1
                
                proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_socket.connect((self.proxy_host, self.proxy_port))
                
                # Send CONNECT request with authentication
                connect_request = f"CONNECT {target} HTTP/1.1\r\n"
                connect_request += f"Host: {target}\r\n"
                connect_request += self.auth_header
                connect_request += "\r\n"
                
                proxy_socket.sendall(connect_request.encode())
                
                # Read response from proxy
                response = proxy_socket.recv(4096)
                
                # Send response to client
                client_socket.sendall(response)
                
                # If connection established, start bidirectional forwarding
                if b"200" in response:
                    self._forward_data(client_socket, proxy_socket)
            else:
                # Bypass proxy - make direct connection
                with self.stats_lock:
                    self.bypassed_count += 1
                
                host, port = target.split(':')
                port = int(port)
                
                # Connect directly to target
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.connect((host, port))
                
                # Send 200 Connection Established to client
                response = b"HTTP/1.1 200 Connection Established\r\n\r\n"
                client_socket.sendall(response)
                
                # Start bidirectional forwarding
                self._forward_data(client_socket, target_socket)
            
        except Exception:
            pass
    
    def _handle_http(self, client_socket, request):
        """Handle regular HTTP request"""
        try:
            # Decode request to extract host
            request_str = request.decode('utf-8', errors='ignore')
            lines = request_str.split('\r\n')
            
            # Extract Host header to determine target
            host = None
            for line in lines:
                if line.lower().startswith('host:'):
                    host = line.split(':', 1)[1].strip()
                    break
            
            # If no Host header found, try to extract from request line
            if not host:
                # For absolute URLs like "GET http://example.com/path HTTP/1.1"
                request_line_parts = lines[0].split(' ')
                if len(request_line_parts) >= 2:
                    url = request_line_parts[1]
                    if url.startswith('http://') or url.startswith('https://'):
                        parsed = urlparse(url)
                        host = parsed.netloc
            
            if not host:
                # Cannot determine host, close connection
                return
            
            # Check if this domain should use the proxy
            if self._should_use_proxy(host):
                # Route through residential proxy
                with self.stats_lock:
                    self.proxied_count += 1
                
                proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_socket.connect((self.proxy_host, self.proxy_port))
                
                # Add authentication header to request
                modified_lines = [lines[0]]
                modified_lines.append(self.auth_header.strip())
                modified_lines.extend(lines[1:])
                
                modified_request = '\r\n'.join(modified_lines).encode('utf-8', errors='ignore')
                
                # Send to upstream proxy
                proxy_socket.sendall(modified_request)
                
                # Forward response back to client
                while True:
                    data = proxy_socket.recv(4096)
                    if not data:
                        break
                    client_socket.sendall(data)
            else:
                # Bypass proxy - make direct connection
                with self.stats_lock:
                    self.bypassed_count += 1
                
                # Parse host and port
                if ':' in host:
                    hostname, port = host.split(':', 1)
                    port = int(port)
                else:
                    hostname = host
                    port = 80
                
                # Connect directly to target
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.connect((hostname, port))
                
                # Send original request (without proxy auth header)
                target_socket.sendall(request)
                
                # Forward response back to client
                while True:
                    data = target_socket.recv(4096)
                    if not data:
                        break
                    client_socket.sendall(data)
            
        except Exception:
            pass
    
    def _forward_data(self, socket1, socket2):
        """Bidirectional data forwarding between two sockets"""
        try:
            while True:
                readable, _, _ = select.select([socket1, socket2], [], [], 1)
                
                if socket1 in readable:
                    data = socket1.recv(4096)
                    if not data:
                        break
                    socket2.sendall(data)
                
                if socket2 in readable:
                    data = socket2.recv(4096)
                    if not data:
                        break
                    socket1.sendall(data)
                    
        except:
            pass

if __name__ == "__main__":
    import time
    
    server = ProxyServer()
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()

