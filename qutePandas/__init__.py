import os
import sys

def _setup_pykx_environment():
    """
    Sets up the environment for PyKX BEFORE any PyKX imports.
    This must run before importing any module that uses PyKX.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(root, ".env")
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key, value = parts
                        value = value.strip().strip('"').strip("'")
                        # Only set if not already in environment
                        if key.strip() and key.strip() not in os.environ:
                            os.environ[key.strip()] = value
    
    # Check for valid license files in priority order
    qutepandas_home = os.path.expanduser("~/.qutepandas")
    local_kdb = os.path.join(root, "kdb_lic")
    
    license_found = False
    valid_license_path = None
    
    if os.path.exists(os.path.join(local_kdb, "kc.lic")):
        valid_license_path = local_kdb
        license_found = True
    elif os.path.exists(os.path.join(qutepandas_home, "kc.lic")):
        valid_license_path = qutepandas_home
        license_found = True
    
    if license_found and valid_license_path:
        os.environ['QLIC'] = valid_license_path
        os.environ.pop('PYKX_UNLICENSED', None)
    elif 'QLIC' in os.environ:
        qlic_path = os.environ['QLIC']
        if not (os.path.exists(os.path.join(qlic_path, "kc.lic")) or 
                os.path.exists(os.path.join(qlic_path, "k4.lic"))):
            del os.environ['QLIC']
            if 'QHOME' in os.environ:
                del os.environ['QHOME']
            license_found = False
    
    if not license_found and 'PYKX_UNLICENSED' not in os.environ:
        os.environ['PYKX_UNLICENSED'] = 'true'
    
    if 'PYKX_RELEASE_GIL' not in os.environ:
        os.environ['PYKX_RELEASE_GIL'] = 'true'
    
    if 'PYKX_ENFORCE_EMBEDDED_IMPORT' not in os.environ:
        os.environ['PYKX_ENFORCE_EMBEDDED_IMPORT'] = '0'

_setup_pykx_environment()

from .core.dataframe import DataFrame
from .core.connection import connect, get_license_info, install_license
from .core.display import py, np, pd, pa, pt, print

from .cleaning.dropna import dropna
from .cleaning.dropna_col import dropna_col
from .cleaning.fillna import fillna
from .cleaning.remove_duplicates import remove_duplicates

from .transformation.cast import cast
from .transformation.drop_col import drop_col
from .transformation.rename import rename

from .joining.merge import merge

from .grouping.groupby_sum import groupby_sum
from .grouping.groupby_avg import groupby_avg

from .io.to_csv import to_csv
from .io.from_csv import from_csv

from .apply.apply import apply
from .apply.apply_col import apply_col

from .introspection.dtypes import dtypes

from .indexing import loc, iloc

__version__ = "1.1.1"