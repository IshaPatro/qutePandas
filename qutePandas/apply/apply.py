import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def apply(df, func, axis=0, return_type='q'):
    """
    Applies function to DataFrame along specified axis.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    func : callable or str
        Function to apply.
    axis : int, default 0
        Axis along which to apply function (0=columns, 1=rows).
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pandas.Series or pykx.Table or pykx.K
        Result of applying function.
    """
    try:
        q_table = _ensure_q_table(df)
        
        if isinstance(func, str):
            if axis == 1:
                result = kx.q(f"{{({func}) each x}}", q_table)
            else:
                result = kx.q(f"{{({func}) each flip x}}", q_table)
                
            return _handle_return(result, return_type)
        else:
            if axis == 1:
                rows = kx.q("{(x)}", q_table)
                res_list = [func(row.pd()) for row in rows]
                result = kx.toq(res_list)
                
            else:
                cols = kx.q("cols", q_table).py()
                
                res_dict = {}
                for col in cols:
                    col_data = kx.q(f"{{x`{col}}}", q_table).pd()
                    res_dict[col] = func(col_data)
                    
                result = kx.toq(res_dict)
            
            return _handle_return(result, return_type)

    except Exception as e:
        raise RuntimeError(f"Failed to apply function: {e}")