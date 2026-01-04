"""
qutePandas - A pandas-like library for q/kdb+
"""

import os

def _setup_environment():
    """Validates and sets up the environment for PyKX."""
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
                        if key.strip():
                            os.environ[key.strip()] = value

    # Priority: Project-local kdb_lic folder
    qutepandas_home = os.path.expanduser("~/.qutepandas")
    local_kdb = os.path.join(root, "kdb_lic")
    
    # Set QLIC to where the license is.
    # Avoid setting QHOME to local_kdb unless it contains all platform files (m64arm).
    # PyKX bundles its own q binaries, so usually only QLIC is needed for license.
    if os.path.exists(os.path.join(local_kdb, "kc.lic")):
        os.environ['QLIC'] = local_kdb
    elif os.path.exists(os.path.join(qutepandas_home, "kc.lic")):
        os.environ['QLIC'] = qutepandas_home

_setup_environment()

from .core.dataframe import DataFrame
from .core.connection import connect, get_license_info, install_license
from .core.display import py, np, pd, pa, pt

from .cleaning.drop_nulls import drop_nulls
from .cleaning.drop_nulls_col import drop_nulls_col
from .cleaning.fill_null import fill_null
from .cleaning.remove_duplicates import remove_duplicates

from .transformation.cast import cast
from .transformation.drop_col import drop_col
from .transformation.rename import rename

from .joining.merge_left import merge_left
from .joining.merge_inner import merge_inner

from .grouping.groupby_sum import groupby_sum
from .grouping.groupby_avg import groupby_avg

from .io.to_csv import to_csv
from .io.from_csv import from_csv

from .apply.apply import apply
from .apply.apply_col import apply_col

__version__ = "1.0.0"
