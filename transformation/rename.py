import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def rename(df, columns, return_type='q'):
    """
    Renames columns in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    columns : dict
        Dictionary mapping old column names to new column names.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with renamed columns.
    """
    try:
        q_table = _ensure_q_table(df)
        
        cols = kx.q("cols", q_table).py()
        new_cols = [columns.get(c, c) for c in cols]
        new_cols_str = "`" + "`".join(new_cols)
        
        result = kx.q(f'{new_cols_str} xcol', q_table)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to rename columns: {e}")
 