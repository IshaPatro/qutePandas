import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def dropna_col(df, col, return_type='q'):
    """
    Drops rows where a specific column is null.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to check for nulls.
    return_type : str, default 'q'
        Desired return type ('p' for pandas, 'q' for kdb+).

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with filtered rows.
    """
    try:
        q_table = _ensure_q_table(df)
        result = kx.q("{[t; c] select from t where not null t c}", q_table, kx.SymbolAtom(col))
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to dropna from column {col}: {e}")