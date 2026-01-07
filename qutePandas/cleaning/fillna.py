import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def fillna(df, col, value, return_type='q'):
    """
    Fills null values in a specific column with a given value.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to fill nulls in.
    value : any
        Value to use for filling nulls.
    return_type : str, default 'q'
        Desired return type ('p' for pandas, 'q' for kdb+).

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with nulls filled.
    """
    try:
        q_table = _ensure_q_table(df)
        if isinstance(value, str):
             fill_val = f'`{value}'
        else:
             fill_val = str(value)
        result = kx.q(f"{{update {col}:{fill_val}^{col} from x}}", q_table)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to fillna in column {col}: {e}")