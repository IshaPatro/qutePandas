import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def apply_col(df, col, func, return_type='q'):
    """
    Applies function to a single column of DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    col : str
        Column name to apply function to.
    func : callable or str
        Function to apply to the column. If string, applied as q function string.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame with function applied to specified column.
    """
    try:
        q_table = _ensure_q_table(df)
        
        if isinstance(func, str):
            result = kx.q(f"{{update {col}:({func}) each {col} from x}}", q_table)
        else:
            col_data = kx.q(f"{{x`{col}}}", q_table).py()
            
            if hasattr(col_data, 'apply'):
                new_data = col_data.apply(func)
            elif isinstance(col_data, list):
                new_data = [func(x) for x in col_data]
            else:
                try:
                    import numpy as np
                    new_data = np.vectorize(func)(col_data)
                except:
                    new_data = [func(x) for x in col_data]
            
            q_new_data = kx.toq(new_data)
            result = kx.q(f"{{update {col}:y from x}}", q_table, q_new_data)
            
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to apply function to column {col}: {e}")
 