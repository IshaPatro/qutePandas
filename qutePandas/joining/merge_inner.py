import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def merge_inner(left, right, keys, return_type='q'):
    """
    Performs inner join on two tables using specified keys.

    Parameters
    ----------
    left : pandas.DataFrame or pykx.Table
        Left DataFrame.
    right : pandas.DataFrame or pykx.Table
        Right DataFrame.
    keys : str or list of str
        Join key column(s).
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        Inner joined DataFrame.
    """
    try:
        q_left = _ensure_q_table(left)
        q_right = _ensure_q_table(right)
        
        if isinstance(keys, str):
            keys = [keys]
        
        key_cols = "`" + "`".join(keys)
        keyed_right = kx.q(f'{key_cols} xkey', q_right)
        
        result = kx.q("{x ij y}", q_left, keyed_right)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to perform inner join: {e}")
 