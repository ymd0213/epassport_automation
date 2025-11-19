"""
Local HTTP proxy server that handles authentication to upstream proxy
This acts as a bridge between Chrome and the authenticated proxy
"""

import socket
import threading
import base64
import select
import os
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
        
        # Create auth header
        credentials = f"{self.proxy_username}:{self.proxy_password}"
        self.auth_header = f"Proxy-Authorization: Basic {base64.b64encode(credentials.encode()).decode()}\r\n"
        
        print(f"Proxy Server Configuration:")
        print(f"  Local: {self.local_host}:{self.local_port}")
        print(f"  Upstream: {self.proxy_host}:{self.proxy_port}")
        print(f"  Auth: {self.proxy_username}:***")
    
    def start(self):
        """Start the proxy server in a background thread"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.local_host, self.local_port))
        self.server_socket.listen(50)
        
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        
        print(f"✅ Proxy server started on {self.local_host}:{self.local_port}")
    
    def stop(self):
        """Stop the proxy server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Proxy server stopped")
    
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
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def _handle_connect(self, client_socket, request_str):
        """Handle HTTPS CONNECT request"""
        try:
            # Extract target host and port
            lines = request_str.split('\r\n')
            target = lines[0].split(' ')[1]
            
            # Connect to upstream proxy
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
            
        except Exception as e:
            print(f"Error in CONNECT: {e}")
    
    def _handle_http(self, client_socket, request):
        """Handle regular HTTP request"""
        try:
            # Connect to upstream proxy
            proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_socket.connect((self.proxy_host, self.proxy_port))
            
            # Add authentication header to request
            request_str = request.decode('utf-8', errors='ignore')
            lines = request_str.split('\r\n')
            
            # Insert auth header after the first line
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
            
        except Exception as e:
            print(f"Error in HTTP: {e}")
    
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
    server = ProxyServer()
    server.start()
    
    print("\nProxy server running. Press Ctrl+C to stop...")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        print("Stopped")

