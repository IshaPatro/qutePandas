"""
Connection and license management for qutePandas.
"""

import os
import pykx as kx
import base64
import shutil


def install_license(content, is_base64=True):
    """
    Installs a kdb+ license into the qutePandas managed directory (~/.qutepandas).
    """
    target_dir = os.path.expanduser("~/.qutepandas")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "kc.lic")
    
    try:
        if is_base64:
            data = base64.b64decode(content)
            with open(target_path, "wb") as f:
                f.write(data)
        else:
            if not os.path.exists(content):
                raise FileNotFoundError(f"License file not found: {content}")
            shutil.copy(content, target_path)
        
        os.environ['QLIC'] = target_dir
        os.environ['QHOME'] = target_dir
        return True
    except Exception as e:
        print(f"✗ Failed to install license: {e}")
        return False


def connect(license_path=None):
    """
    Connect to kdb+ with specified license.
    """
    try:
        if license_path:
            os.environ['QLIC'] = license_path
            os.environ['QHOME'] = license_path
            os.environ['PYKX_Q_LIB_LOCATION'] = license_path
            kx.q('1+1')
            return True
            
        possible_paths = [
            '/Applications/kdb+:q',
            os.path.expanduser("~/.qutepandas"),
            os.path.expanduser("~/kdb+"),
            os.path.expanduser("~/q"),
            os.path.expanduser("~/.pykx")
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, "kc.lic")) or os.path.exists(os.path.join(path, "k4.lic")):
                os.environ['QLIC'] = path
                os.environ['QHOME'] = path
                os.environ['PYKX_Q_LIB_LOCATION'] = path
                try:
                    kx.q('1+1')
                    print(f"✓ Successfully connected using license from: {path}")
                    return True
                except:
                    continue
        
        print("✗ Failed to connect to kdb+: No valid license found.")
        print("\nTo resolve this Issue:")
        print("1. Apply for a free kdb+ license at https://kx.com/connect-with-us/download/")
        print("2. Once you have the license, install it using qutePandas:")
        print("   >>> import qutePandas as qpd")
        print("   >>> qpd.install_license('your-base64-license-string-here')")
        return False
        
    except Exception as e:
        print(f"✗ Failed to connect to kdb+: {e}")
        return False


def get_license_info():
    """
    Get information about the current kdb+ license setup.
    """
    try:
        qlic_path = os.environ.get('QLIC', 'Not set')
        qhome_path = os.environ.get('QHOME', 'Not set')
        kx.q('1+1')
        
        return {
            'qlic_path': qlic_path,
            'qhome_path': qhome_path,
            'connection_status': 'Connected'
        }
    except Exception as e:
        return {
            'qlic_path': os.environ.get('QLIC', 'Not set'),
            'qhome_path': os.environ.get('QHOME', 'Not set'),
            'connection_status': 'Failed',
            'error': str(e)
        }
