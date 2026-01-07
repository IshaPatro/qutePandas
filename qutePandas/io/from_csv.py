import pykx as kx
import pandas as pd
from ..utils import _handle_return

def from_csv(path, return_type='q'):
    """
    Imports DataFrame from CSV file.

    Parameters
    ----------
    path : str
        File path to load CSV from.
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        Loaded DataFrame.
    """
    try:
        df = pd.read_csv(path)
        q_table = kx.toq(df)
        return _handle_return(q_table, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV file {path}: {e}")