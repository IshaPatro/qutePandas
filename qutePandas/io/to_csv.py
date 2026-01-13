import pykx as kx
import pandas as pd
import pyarrow.csv as pa_csv
from ..utils import _ensure_q_table

def to_csv(df, path):
    """
    Exports DataFrame to CSV file.

    Parameters
    ----------
    df : pandas.DataFrame or pykx.Table
        Input DataFrame.
    path : str
        File path to save CSV.

    Returns
    -------
    str
        Success message.
    """
    try:
        if hasattr(df, 'pa'):
            pa_tab = df.pa()
            pa_csv.write_csv(pa_tab, path)
            return f"Table saved to: {path}"
        
        if isinstance(df, (kx.Table, kx.KeyedTable)):
            pd_df = df.pd()
        elif isinstance(df, pd.DataFrame):
            pd_df = df
        else:
            pd_df = pd.DataFrame(df)
            
        pd_df.to_csv(path, index=False)
        return f"Table saved to: {path}"

    except Exception as e:
        raise RuntimeError(f"Failed to save table to CSV: {e}")