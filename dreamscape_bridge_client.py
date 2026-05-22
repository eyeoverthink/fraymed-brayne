"""
Dreamscape Bridge Client - Python client for Java-Python bridge

Connects to DreamscapeBridge.java to extract real-time FRAYMUS states.
"""

import socket
import json
import time
from typing import Dict, Any, Optional


class DreamscapeBridgeClient:
    """Client for connecting to DreamscapeBridge Java server"""
    
    def __init__(self, host: str = "localhost", port: int = 42100):
        """
        Initialize bridge client
        
        Args:
            host: Server hostname (default: localhost)
            port: Server port (default: 42100)
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to DreamscapeBridge server
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"[DreamscapeClient] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"[DreamscapeClient] Connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            self.socket.close()
            self.connected = False
            print("[DreamscapeClient] Disconnected")
    
    def send_command(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Send command to server and parse JSON response
        
        Args:
            command: Command string (e.g., "status", "extract", "help")
        
        Returns:
            Parsed JSON response, or None if error
        """
        if not self.connected:
            print("[DreamscapeClient] Not connected to server")
            return None
        
        try:
            # Send command
            self.socket.sendall((command + "\n").encode('utf-8'))
            
            # Receive response
            response = self.socket.recv(65536).decode('utf-8')
            
            # Parse JSON
            return json.loads(response)
            
        except Exception as e:
            print(f"[DreamscapeClient] Error sending command: {e}")
            return None
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        Get bridge status
        
        Returns:
            Status dictionary
        """
        return self.send_command("status")
    
    def extract_states(self) -> Optional[Dict[str, Any]]:
        """
        Extract all FRAYMUS states
        
        Returns:
            Dictionary containing all extracted states
        """
        return self.send_command("extract")
    
    def get_help(self) -> Optional[Dict[str, Any]]:
        """
        Get help information
        
        Returns:
            Help dictionary
        """
        return self.send_command("help")


def test_connection():
    """Test connection to DreamscapeBridge"""
    client = DreamscapeBridgeClient()
    
    if client.connect():
        # Get status
        status = client.get_status()
        if status:
            print("[Test] Status:", json.dumps(status, indent=2))
        
        # Extract states
        states = client.extract_states()
        if states:
            print("[Test] States extracted successfully")
            print(f"[Test] Timestamp: {states.get('timestamp')}")
            print(f"[Test] Phi: {states.get('phi')}")
            print(f"[Test] Visual prompt: {states.get('visual_prompt')}")
        
        client.disconnect()
    else:
        print("[Test] Could not connect to DreamscapeBridge")
        print("[Test] Make sure DreamscapeBridge.java is running on port 42100")


if __name__ == "__main__":
    test_connection()
