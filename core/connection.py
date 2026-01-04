"""
Connection and license management for qutePandas.
Enforces strict license validation with fail-fast behavior.
"""

import os
import pykx as kx
import base64
import shutil


def _get_project_lic_dir():
    """Get the project-local license directory."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "kdb_lic")


def install_license(content, is_base64=True):
    """
    Installs a kdb+ license from base64 content or file path.
    Prioritizes project-local folder 'kdb_lic' if it exists.
    Returns True on success, raises RuntimeError on failure.
    """
    target_dir = _get_project_lic_dir()
    if not os.path.exists(target_dir):
        target_dir = os.path.expanduser("~/.qutepandas")
        
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "kc.lic")
    
    content = content.strip().strip('"').strip("'")
    
    if is_base64:
        padding = len(content) % 4
        if padding:
            content += "=" * (4 - padding)
        content = content.replace('-', '+').replace('_', '/')
        
        try:
            data = base64.b64decode(content)
        except Exception as e:
            raise RuntimeError(f"Invalid base64 license content: {e}")
            
        try:
            text_data = data.decode('utf-8')
            if text_data.startswith('0001'):
                os.environ['KX_TOKEN'] = text_data
                os.environ['QTOK'] = text_data
                if os.path.exists(target_path):
                    os.remove(target_path)
                return True
        except:
            pass
            
        with open(target_path, "wb") as f:
            f.write(data)
    else:
        if not os.path.exists(content):
            raise RuntimeError(f"License file not found: {content}")
        shutil.copy(content, target_path)
    
    os.environ['QLIC'] = target_dir
    return True


def connect(license_path=None):
    """
    Establishes connection to kdb+.
    Raises RuntimeError if license is invalid or missing.
    """
    if license_path:
        if not os.path.exists(license_path):
            raise RuntimeError(f"License path does not exist: {license_path}")
        os.environ['QLIC'] = license_path
    
    # Try immediate connection
    try:
        kx.q('1+1')
        return True
    except:
        pass
    
    # Try token
    token = (os.environ.get('KDB_TOKEN') or os.environ.get('KX_TOKEN', '')).strip()
    if token:
        install_license(token)
        try:
            kx.q('1+1')
            return True
        except:
            pass
    
    # Search paths
    possible_paths = [
        _get_project_lic_dir(),
        os.path.expanduser("~/.qutepandas"),
        '/Applications/kdb+:q',
        os.path.expanduser("~/kdb+"),
        os.path.expanduser("~/q"),
        os.path.expanduser("~/.pykx")
    ]
    
    for path in possible_paths:
        if not os.path.exists(path):
            continue
            
        if os.path.exists(os.path.join(path, "kc.lic")) or os.path.exists(os.path.join(path, "k4.lic")):
            os.environ['QLIC'] = path
            try:
                kx.q('1+1')
                return True
            except:
                continue
    
    raise RuntimeError(
        "No valid kdb+ license found. "
        "Set KDB_TOKEN in .env or place kc.lic in local kdb_lic/ or ~/.qutepandas/"
    )


def get_license_info():
    """
    Returns current license configuration status.
    """
    try:
        kx.q('1+1')
        return {
            'qlic_path': os.environ.get('QLIC', 'Not set'),
            'qhome_path': os.environ.get('QHOME', 'Not set'),
            'kx_token_set': 'Yes' if os.environ.get('KX_TOKEN') else 'No',
            'connection_status': 'Connected'
        }
    except Exception as e:
        return {
            'qlic_path': os.environ.get('QLIC', 'Not set'),
            'qhome_path': os.environ.get('QHOME', 'Not set'),
            'kx_token_set': 'Yes' if os.environ.get('KX_TOKEN') else 'No',
            'connection_status': 'Failed',
            'error': str(e)
        }
