import pykx as kx
import pandas as pd
from qutePandas.utils import _ensure_q_table, _handle_return


def groupby_sum(df, by_cols, sum_col, return_type='q'):
    """
    Groups table by specified column(s) and sums target column.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    by_cols : str or list of str
        Group by column(s).
    sum_col : str
        Column to sum.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        Grouped and summed DataFrame.
    """
    try:
        q_table = _ensure_q_table(df)
        if isinstance(by_cols, str):
            by_cols = [by_cols]
        
        by_clause = ",".join(by_cols)
        
        result = kx.q(f"{{select sum {sum_col} by {by_clause} from x}}", q_table)
        
        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to group by sum: {e}")
 