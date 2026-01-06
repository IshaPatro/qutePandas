import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return

def dropna_col(df, col, return_type='q'):
    try:
        q_table = _ensure_q_table(df)
        result = kx.q("{[t; c] select from t where not null t c}", q_table, kx.SymbolAtom(col))
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to dropna from column {col}: {e}")