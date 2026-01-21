"""
apply - Function application for qutePandas DataFrames.

Performance Optimization Notes:
------------------------------
For row-wise operations (axis=1) with Python callables, this module now uses
direct numpy array iteration instead of pandas `iterrows()`. This provides
significant speedup as `iterrows()` creates a new Series object per row.

Previous approach: for _, row in pdf.iterrows() -> func(row)  [~100x slower]
Optimized approach: for row in pdf.values -> func(row)  [direct numpy iteration]

Note: String functions (e.g., 'sum', 'avg') still execute entirely in kdb+
using `each` for maximum performance. The optimization only affects Python
callable functions where data must cross the Python/q boundary.
"""

import pykx as kx
import pandas as pd
import numpy as np
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
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pandas.Series or pykx.Table or pykx.K
        Result of applying function.
    """
    try:
        q_table = _ensure_q_table(df)
        
        if len(q_table) == 0:
            if axis == 1:
                return _handle_return(kx.toq([]), return_type)
            if not isinstance(func, str):
                pdf = df if isinstance(df, pd.DataFrame) else q_table.pd()
                return pdf.apply(func, axis=axis)
            elif func == "sum":
                cols = kx.q("cols", q_table).py()
                result = kx.toq({c: 0 for c in cols})
                ret = _handle_return(result, return_type)
                return pd.Series(ret) if return_type == 'p' else ret

        if isinstance(func, str):
            if axis == 1:
                result = kx.q(f"{{({func}) each x}}", q_table)
            else:
                result = kx.q(f"{{({func}) each flip x}}", q_table)
                

        else:
            if axis == 1:
                pdf = q_table.pd()
                # Use numpy arrays directly - much faster than iterrows()
                # Apply function to each row as a numpy array
                values = pdf.values
                col_names = pdf.columns.tolist()

                # Try fast path with raw numpy arrays first
                try:
                    # Attempt to apply directly to numpy rows (fastest)
                    res_list = [func(row) for row in values]
                except (TypeError, ValueError):
                    # Fall back to Series if function requires it (e.g., uses column names)
                    res_list = [func(pd.Series(row, index=col_names)) for row in values]

                result = kx.toq(res_list)

            else:
                cols = kx.q("cols", q_table).py()

                res_dict = {}
                for col in cols:
                    col_data = kx.q(f"{{x`{col}}}", q_table).pd()
                    res_dict[col] = func(col_data)

                result = kx.toq(res_dict)
            
        ret = _handle_return(result, return_type)
        if return_type == 'p' and isinstance(ret, dict):
            return pd.Series(ret)
        return ret

    except Exception as e:
        raise RuntimeError(f"Failed to apply function: {e}")