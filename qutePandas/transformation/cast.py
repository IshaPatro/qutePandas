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

        if len(q_type) != 1:
            raise ValueError(f"Unsupported q cast type: {dtype}")

        curr_type = kx.q(f'{{type x`{col}}}', q_table).py()
        type_to_code = {
            'j': 7, 'i': 6, 'h': 5, 'f': 9, 'e': 8, 's': 11, 'c': 10, 'b': 1
        }
        target_code = type_to_code.get(q_type.lower())

        if target_code is not None and abs(curr_type) == target_code:
            return _handle_return(q_table, return_type)

        is_parsing = curr_type in (0, 10)
        q_char = q_type.upper() if is_parsing else q_type.lower()

        if q_char.lower() == 's':
            result = kx.q(
                f'{{update {col}:`$ string {col} from x}}',
                q_table
            )
        elif q_char in ('i', 'j'):
            result = kx.q(
                f'{{update {col}:"{q_char}"$(({col}>=0)*floor {col} + ({col}<0)*ceiling {col}) from x}}',
                q_table
            )
        else:
            result = kx.q(
                f'{{update {col}:"{q_char}"${col} from x}}',
                q_table
            )

        return _handle_return(result, return_type)

    except Exception as e:
        raise RuntimeError(f"Failed to cast column {col} to type {dtype}: {e}")
