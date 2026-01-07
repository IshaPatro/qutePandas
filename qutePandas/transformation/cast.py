import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def cast(df, col, dtype, return_type='q'):
    """
    Converts column to specified data type.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to cast.
    dtype : str
        Target data type ('i' for int, 'f' for float, 's' for symbol, etc.).
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with column cast to new type.
    """
    try:
        q_map = {
            'int64': 'j', 'int32': 'i', 'int': 'i', 'long': 'j',
            'float64': 'f', 'float32': 'e', 'float': 'f', 'real': 'e',
            'object': 's', 'string': 'C', 'str': 'C',
            'j': 'j', 'i': 'i', 'h': 'h', 'f': 'f', 'e': 'e', 's': 's', 'c': 'c'
        }
        
        q_type = q_map.get(dtype, dtype)
        q_table = _ensure_q_table(df)
        
        if len(q_type) == 1:
            is_parsing = kx.q(f'{{(type x`{col}) in 0 10 11h}}', q_table).py()
            q_char = q_type.upper() if is_parsing else q_type.lower()
            result = kx.q(f'{{update {col}:"{q_char}"${col} from x}}', q_table)
        else:
             raise ValueError(f"Unsupported q cast type: {dtype}")

        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to cast column {col} to type {dtype}: {e}")