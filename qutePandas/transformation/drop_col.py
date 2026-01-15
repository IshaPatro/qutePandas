import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return, _validate_columns


def drop_col(df, cols, return_type='q'):
    """
    Removes specified column(s) from the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    cols : list of str or str
        Column names to drop.
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with specified column(s) removed.
    """
    try:
        q_table = _ensure_q_table(df)

        if isinstance(cols, str):
            cols = [cols]

        if not isinstance(cols, (list, tuple)):
            raise ValueError("cols must be a list of column names")

        if not cols:
            return _handle_return(q_table, return_type)

        _validate_columns(q_table, cols)
        
        all_cols = kx.q("cols", q_table).py()
        if len(cols) == len(all_cols):
            if return_type == 'p':
                count = kx.q('count', q_table).py()
                return pd.DataFrame(index=range(count))
            else:
                result = kx.q('(0#`)!()')
                return result
        else:
            q_cols = kx.SymbolVector(cols)
            result = kx.q('{[t;c] ![t;();0b;(),c]}', q_table, q_cols)

        return _handle_return(result, return_type)

    except Exception as e:
        raise RuntimeError(f"Failed to drop columns {cols}: {e}")