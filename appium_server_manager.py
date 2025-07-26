#!/usr/bin/env python3
"""
Appium Server Manager
Handles starting, stopping, and monitoring Appium server instances
"""

import subprocess
import requests
import signal
import os
import time
import logging
from typing import Optional


class AppiumServerManager:
    """Manages Appium server lifecycle"""
    
    def __init__(self, host: str = "localhost", port: int = 4723, logger: Optional[logging.Logger] = None):
        """
        Initialize Appium Server Manager
        
        Args:
            host: Appium server host (default: localhost)
            port: Appium server port (default: 4723)
            logger: Logger instance (optional)
        """
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger(__name__)
        self.appium_process: Optional[subprocess.Popen] = None
        self.server_url = f"http://{self.host}:{self.port}"
        self.status_url = f"{self.server_url}/wd/hub/status"
    
    def is_server_running(self) -> bool:
        """
        Check if Appium server is running
        
        Returns:
            bool: True if server is running and responding, False otherwise
        """
        try:
            # Try multiple endpoints for better detection
            endpoints_to_try = [
                f"http://{self.host}:{self.port}/wd/hub/status",
                f"http://{self.host}:{self.port}/status",
                f"http://{self.host}:{self.port}/wd/hub/sessions"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = requests.get(endpoint, timeout=3)
                    # Accept any successful HTTP response (200-299)
                    if 200 <= response.status_code < 300:
                        self.logger.info(f"Appium server is running on {self.host}:{self.port} (detected via {endpoint})")
                        return True
                    elif response.status_code == 404:
                        # 404 might mean server is running but endpoint doesn't exist
                        # Try next endpoint
                        continue
                except requests.exceptions.RequestException:
                    # Try next endpoint
                    continue
            
            # If all endpoints failed, try a simple connection test
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.host, self.port))
                sock.close()
                
                if result == 0:
                    self.logger.info(f"Appium server detected on {self.host}:{self.port} (port is open)")
                    return True
            except Exception:
                pass
                
            self.logger.info(f"Appium server is not running on {self.host}:{self.port}")
            return False
                
        except Exception as e:
            self.logger.error(f"Error checking server status: {str(e)}")
            return False
    
    def start_server(self, timeout: int = 30) -> bool:
        """
        Start Appium server if not running
        
        Args:
            timeout: Maximum time to wait for server startup (seconds)
            
        Returns:
            bool: True if server started successfully, False otherwise
        """
        try:
            self.logger.info(f"Starting Appium server on {self.host}:{self.port}...")
            
            # Build Appium command (Appium 2.x syntax)
            cmd = ['appium', '--port', str(self.port)]
            
            # Add address parameter for non-localhost hosts
            if self.host != 'localhost' and self.host != '127.0.0.1':
                cmd.extend(['--address', self.host])
            
            # Start the process with output redirection
            self.appium_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                preexec_fn=os.setsid  # Create new process group for clean termination
            )
            
            # Wait for server to start
            wait_interval = 2
            elapsed = 0
            
            while elapsed < timeout:
                if self.is_server_running():
                    self.logger.info(f"Appium server started successfully in {elapsed}s")
                    return True
                
                time.sleep(wait_interval)
                elapsed += wait_interval
                
                # Check if process is still running
                if self.appium_process.poll() is not None:
                    stdout, stderr = self.appium_process.communicate()
                    self.logger.error(f"Appium server failed to start. Error: {stderr}")
                    self.appium_process = None
                    return False
            
            self.logger.error(f"Appium server failed to start within {timeout} seconds")
            self.stop_server()
            return False
            
        except FileNotFoundError:
            self.logger.error("Appium not found. Please install Appium: npm install -g appium")
            return False
        except Exception as e:
            self.logger.error(f"Failed to start Appium server: {str(e)}")
            return False
    
    def stop_server(self) -> bool:
        """
        Stop Appium server if we started it
        
        Returns:
            bool: True if server stopped successfully, False otherwise
        """
        if not self.appium_process:
            self.logger.info("No Appium server process to stop")
            return True
            
        try:
            self.logger.info("Stopping Appium server...")
            
            # Kill the entire process group
            os.killpg(os.getpgid(self.appium_process.pid), signal.SIGTERM)
            
            # Wait for process to terminate gracefully
            try:
                self.appium_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                self.logger.warning("Appium server didn't stop gracefully, force killing...")
                os.killpg(os.getpgid(self.appium_process.pid), signal.SIGKILL)
                self.appium_process.wait()
            
            self.logger.info("Appium server stopped successfully")
            self.appium_process = None
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping Appium server: {str(e)}")
            return False
    
    def ensure_server_running(self, start_timeout: int = 30) -> bool:
        """
        Ensure Appium server is running, start if needed
        
        Args:
            start_timeout: Maximum time to wait for server startup if needed (seconds)
            
        Returns:
            bool: True if server is running (was already running or started successfully)
        """
        if self.is_server_running():
            return True
        
        return self.start_server(timeout=start_timeout)
    
    def get_server_info(self) -> dict:
        """
        Get server information and status
        
        Returns:
            dict: Server information including host, port, status, and process info
        """
        info = {
            'host': self.host,
            'port': self.port,
            'server_url': self.server_url,
            'is_running': self.is_server_running(),
            'managed_process': self.appium_process is not None,
            'process_id': self.appium_process.pid if self.appium_process else None
        }
        
        return info
    
    def restart_server(self, timeout: int = 30) -> bool:
        """
        Restart Appium server (stop if running, then start)
        
        Args:
            timeout: Maximum time to wait for server startup (seconds)
            
        Returns:
            bool: True if server restarted successfully
        """
        self.logger.info("Restarting Appium server...")
        
        # Stop server if we're managing it
        if self.appium_process:
            if not self.stop_server():
                self.logger.error("Failed to stop Appium server for restart")
                return False
        
        # Start server
        return self.start_server(timeout=timeout)
    
    def __enter__(self):
        """Context manager entry"""
        self.ensure_server_running()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.stop_server()


# Convenience functions for simple usage
def start_appium_server(host: str = "localhost", port: int = 4723, timeout: int = 30, logger: Optional[logging.Logger] = None) -> AppiumServerManager:
    """
    Start Appium server and return manager instance
    
    Args:
        host: Appium server host
        port: Appium server port
        timeout: Maximum time to wait for startup
        logger: Logger instance
        
    Returns:
        AppiumServerManager: Manager instance with running server
        
    Raises:
        RuntimeError: If server fails to start
    """
    manager = AppiumServerManager(host=host, port=port, logger=logger)
    
    if not manager.ensure_server_running(start_timeout=timeout):
        raise RuntimeError(f"Failed to start Appium server on {host}:{port}")
    
    return manager


def is_appium_running(host: str = "localhost", port: int = 4723) -> bool:
    """
    Quick check if Appium server is running
    
    Args:
        host: Appium server host
        port: Appium server port
        
    Returns:
        bool: True if server is running
    """
    manager = AppiumServerManager(host=host, port=port)
    return manager.is_server_running()


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
    
    # Example 1: Basic usage
    print("=== Basic Appium Server Management ===")
    manager = AppiumServerManager()
    
    print(f"Server running: {manager.is_server_running()}")
    
    if manager.ensure_server_running():
        print("Server is now running!")
        print(f"Server info: {manager.get_server_info()}")
        
        # Do some work here...
        time.sleep(2)
        
        manager.stop_server()
    else:
        print("Failed to start server")
    
    print("\n=== Context Manager Usage ===")
    # Example 2: Context manager usage
    try:
        with AppiumServerManager() as server_manager:
            print("Server is running within context")
            print(f"Server info: {server_manager.get_server_info()}")
            # Server will be automatically stopped when exiting context
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Convenience Function Usage ===")
    # Example 3: Convenience function
    try:
        server_manager = start_appium_server()
        print("Server started using convenience function")
        server_manager.stop_server()
    except RuntimeError as e:
        print(f"Failed to start server: {e}")
