"""
Connection management for qutePandas.

This module provides functions to connect to kdb+ with license management.
"""

import os
import pykx as kx


def connect(license_path=None):
    """
    Connect to kdb+ with specified license.
    
    Sets up the kdb+ environment with the provided license file.
    
    Parameters
    ----------
    license_path : str, optional
        Path to the directory containing the kdb+ license file.
        If None, uses default locations in order:
        1. ~/.qutepandas (recommended for Personal Edition)
        2. /Applications/kdb+:q (standard macOS installation)
        
    Returns
    -------
    bool
        True if connection successful, False otherwise.
        
    Example
    -------
    >>> import qutePandas as qpd
    >>> qpd.connect()  # Uses default license locations
    >>> df = qpd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    """
    try:
        if license_path is None:
            possible_paths = [
                os.path.expanduser("~/.qutepandas"),
                os.path.expanduser("~/kdb+"),
                os.path.expanduser("~/q"),
                os.path.expanduser("~/.pykx"),
                '/Applications/kdb+:q'
            ]
            for path in possible_paths:
                if os.path.exists(os.path.join(path, "kc.lic")) or os.path.exists(os.path.join(path, "k4.lic")):
                    license_path = path
                    break
            
            if license_path is None:
                license_path = '/Applications/kdb+:q'
            
        os.environ['QLIC'] = license_path
        os.environ['QHOME'] = license_path
        
        test_result = kx.q('1+1')
        print(f"✓ Successfully connected to kdb+. Test result: {test_result}")
        print(f"✓ Using license from: {license_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to connect to kdb+: {e}")
        print("Please ensure:")
        print("1. kdb+ license is properly set up")
        print("2. Run the license setup script: python setup_license.py")
        print("3. Or manually set license path: qpd.connect('/path/to/license')")
        print(f"4. Tried license path: {license_path}")
        return False


def get_license_info():
    """
    Get information about the current kdb+ license setup.
    
    Returns
    -------
    dict
        Dictionary containing license information.
    """
    try:
        qlic_path = os.environ.get('QLIC', 'Not set')
        qhome_path = os.environ.get('QHOME', 'Not set')
        test_result = kx.q('1+1')
        
        return {
            'qlic_path': qlic_path,
            'qhome_path': qhome_path,
            'connection_status': 'Connected',
            'test_result': str(test_result)
        }
    except Exception as e:
        return {
            'qlic_path': os.environ.get('QLIC', 'Not set'),
            'qhome_path': os.environ.get('QHOME', 'Not set'),
            'connection_status': 'Failed',
            'error': str(e)
        } 