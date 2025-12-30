import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def drop_col(df, cols, return_type='q'):
    """
    Removes specified column(s) from the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    cols : str or list of str
        Column name(s) to drop.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with specified column(s) removed.
    """
    try:
        q_table = _ensure_q_table(df)
        if isinstance(cols, str):
            cols = [cols]
        
        if cols:
            result = kx.q(f"{{delete {','.join(cols)} from x}}", q_table)
        else:
            result = q_table
            
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to drop columns {cols}: {e}")
 