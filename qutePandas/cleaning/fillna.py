import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def fillna(df, values, return_type='q'):
    """
    Fills null values using a dictionary mapping of columns to fill values.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    values : dict
        Mapping of column names to fill values.
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with nulls filled.
    """
    try:
        if not isinstance(values, dict):
            raise ValueError("values must be a dictionary")

        q_table = _ensure_q_table(df)
        result = q_table

        for col, val in values.items():
            fill_val = f'`{val}' if isinstance(val, str) else str(val)
            result = kx.q(f"{{update {col}:{fill_val}^{col} from x}}", result)

        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to fillna: {e}")
