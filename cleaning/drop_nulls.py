import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def drop_nulls(df, return_type='q'):
    """
    Removes all rows from the DataFrame that contain null values in any column.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with null rows removed.
    """
    try:
        q_table = _ensure_q_table(df)
        result = kx.q("{select from x where not any null each value flip x}", q_table)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to drop nulls from table: {e}")
 