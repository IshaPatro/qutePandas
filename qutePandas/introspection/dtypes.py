import pykx as kx
from ..utils import _ensure_q_table, _handle_return

def dtypes(df, return_type='q'):
    """
    Returns the data types of each column in the DataFrame.
    """
    try:
        q_table = _ensure_q_table(df)
        res = kx.q("{meta x}", q_table)
        return _handle_return(res, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve data types: {e}")
