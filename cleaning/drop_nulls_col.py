import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def drop_nulls_col(df, col, return_type='q'):
    """
    Removes rows from the DataFrame that contain null values in the specified column.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to check for nulls.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with null rows removed from specified column.
    """
    try:
        q_table = _ensure_q_table(df)
        result = kx.q("{[t; c] select from t where not null t c}", q_table, kx.SymbolAtom(col))
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to drop nulls from column {col}: {e}")