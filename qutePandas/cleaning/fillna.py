import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def fillna(df, col_or_values, fill_value=None, return_type='q'):
    """
    Fills null values in specified columns.

    Can be called in two ways:
        fillna(df, values_dict, return_type='q')
        fillna(df, col_name, fill_value, return_type='q')

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col_or_values : str or dict
        If str, the column name to fill (requires fill_value).
        If dict, a mapping of column names to fill values.
    fill_value : scalar, optional
        The value to fill nulls with when col_or_values is a column name.
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with nulls filled.
    """
    try:
        if isinstance(col_or_values, str):
            if fill_value is None:
                raise ValueError("fill_value is required when col_or_values is a column name")
            values = {col_or_values: fill_value}
        elif isinstance(col_or_values, dict):
            values = col_or_values
        else:
            raise ValueError("col_or_values must be a column name (str) or a dictionary")

        q_table = _ensure_q_table(df)
        result = q_table

        for col, val in values.items():
            fill_val = f'`{val}' if isinstance(val, str) else str(val)
            result = kx.q(f"{{update {col}:{fill_val}^{col} from x}}", result)

        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to fillna: {e}")