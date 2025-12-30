import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def fill_null(df, col, value, return_type='q'):
    """
    Fills null values in the specified column with the given value.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to fill nulls.
    value : any
        Value to fill nulls with.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with nulls filled in the specified column.
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
        raise RuntimeError(f"Failed to fill nulls in column {col}: {e}")
 