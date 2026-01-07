import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def groupby_avg(df, by_cols, avg_col, return_type='q'):
    """
    Groups table by specified column(s) and averages target column.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    by_cols : str or list of str
        Group by column(s).
    avg_col : str
        Column to average.
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        Grouped and averaged DataFrame.
    """
    try:
        q_table = _ensure_q_table(df)
        if isinstance(by_cols, str):
            by_cols = [by_cols]
        
        from ..utils import _validate_columns
        _validate_columns(q_table, by_cols + [avg_col])
        by_clause = ",".join(by_cols)
        
        keyed_result = kx.q(f"{{select avg {avg_col} by {by_clause} from x}}", q_table)
        result = kx.q("{0!x}", keyed_result)
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to group by avg: {e}")
 