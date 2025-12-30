"""
KDB+ Connection Manager for qutePandas.

This module handles connections to kdb+ processes and provides utilities
for executing q code and converting between Python and q data structures.
"""

import os
import subprocess
import time
import atexit
from qpython import qconnection
from qpython.qtype import QException


class QConnectionManager:
    """Manages connection to a kdb+ process for qutePandas operations."""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.q_process = None
        self.connection = None
        self._ensure_q_process()
        self._connect()
        
    def _ensure_q_process(self):
        """Start a q process if not already running."""
        try:
            # Try to connect to existing process
            test_conn = qconnection.QConnection(host=self.host, port=self.port)
            test_conn.open()
            test_conn.close()
            return  # Process already running
        except:
            # Need to start q process
            self._start_q_process()
            
    def _start_q_process(self):
        """Start a new q process with the qutePandas.q file loaded."""
        q_script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'qutePandas.q')
        q_script_path = os.path.abspath(q_script_path)
        
        cmd = ['q', '-p', str(self.port), q_script_path]
        
        try:
            self.q_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Give q process time to start
            time.sleep(2)
            
            # Register cleanup
            atexit.register(self._cleanup)
            
        except FileNotFoundError:
            print("Warning: q/kdb+ not found. Using fallback pandas implementation.")
            print("To use kdb+ backend, please install kdb+ and ensure 'q' is in PATH.")
            self.q_process = None
            
    def _connect(self):
        """Establish connection to q process."""
        if self.q_process is None:
            return None
            
        try:
            self.connection = qconnection.QConnection(host=self.host, port=self.port)
            self.connection.open()
            return self.connection
        except Exception as e:
            print(f"Warning: Could not connect to q process: {e}")
            self.connection = None
            return None
            
    def execute(self, query, *args):
        """Execute a q query and return the result."""
        if self.connection is None:
            raise RuntimeError("No active q connection. Falling back to pandas.")
            
        try:
            if args:
                return self.connection(query, *args)
            else:
                return self.connection(query)
        except QException as e:
            raise RuntimeError(f"Q execution error: {e}")
            
    def _cleanup(self):
        """Clean up q process and connection."""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
                
        if self.q_process:
            try:
                self.q_process.terminate()
                self.q_process.wait(timeout=5)
            except:
                try:
                    self.q_process.kill()
                except:
                    pass


# Global connection instance
_global_q_connection = None


def get_q_connection():
    """Get or create the global q connection."""
    global _global_q_connection
    if _global_q_connection is None:
        _global_q_connection = QConnectionManager()
    return _global_q_connection


def execute_q(query, *args):
    """Execute a q query using the global connection."""
    conn = get_q_connection()
    return conn.execute(query, *args) 