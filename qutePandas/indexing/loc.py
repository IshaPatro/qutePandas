import pykx as kx
from ..utils import _ensure_q_table, _handle_return, _validate_columns

def loc(df, rows=None, cols=None, return_type='q'):
    """
    Pure label-location based indexing for selection by label (or boolean array).
    
    Parameters
    ----------
    df : pykx.Table or pd.DataFrame
        Input data.
    rows : list of bool, pykx.BooleanVector, or None
        Boolean mask for row selection.
    cols : str, list of str, or None
        Column names to select.
    return_type : str, default 'q'
        'q' for pykx.Table, 'p' for pandas DataFrame.
        
    Returns
    -------
    pykx.Table or pd.DataFrame
        Subset of the inputs.
    """
    table = _ensure_q_table(df)
    
    q_rows = None
    if rows is not None:
        if isinstance(rows, list):
            q_rows = kx.toq(rows)
        else:
            q_rows = rows
             
    q_cols = None
    if cols is not None:
        if isinstance(cols, str):
            cols = [cols]
        _validate_columns(table, cols)
        syms = kx.SymbolVector(cols)
        q_cols = kx.q('!', syms, syms)
        
    if q_rows is not None and q_cols is not None:
        q_res = kx.q("{?[x;enlist y;0b;z]}", table, q_rows, q_cols)
        
    elif q_rows is not None:
        q_res = kx.q("{?[x;enlist y;0b;()]}", table, q_rows)
        
    elif q_cols is not None:
        q_res = kx.q("{?[x;();0b;y]}", table, q_cols)
        
    else:
        q_res = table
        
    return _handle_return(q_res, return_type)
