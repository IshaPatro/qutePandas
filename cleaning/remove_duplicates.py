import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def remove_duplicates(df, return_type='q'):
    """
    Removes duplicate rows from the DataFrame, keeping the first occurrence.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with duplicate rows removed.
    """
    try:
        q_table = _ensure_q_table(df)
        result = kx.q("{distinct x}", q_table)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to remove duplicates from table: {e}")
 