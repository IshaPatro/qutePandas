import pykx as kx
from qutePandas.utils import _ensure_q_table

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
        q_table = _ensure_q_table(df)
        kx.q(f"{{`:{path} 0: csv 0: x}}", q_table)
        return f"Table saved to: {path}"
    except Exception as e:
        raise RuntimeError(f"Failed to save table to CSV: {e}")