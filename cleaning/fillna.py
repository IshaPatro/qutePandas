import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def fillna(df, col, value, return_type='q'):
    try:
        q_table = _ensure_q_table(df)
        if isinstance(value, str):
             fill_val = f'`{value}'
        else:
             fill_val = str(value)
        result = kx.q(f"{{update {col}:{fill_val}^{col} from x}}", q_table)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to fillna in column {col}: {e}")