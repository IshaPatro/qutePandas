import pykx as kx
from ..utils import _ensure_q_table, _handle_return, _validate_columns

def iloc(df, rows=None, cols=None, return_type='q'):
    """
    Pure integer-location based indexing for selection by position.
    
    Parameters
    ----------
    df : pykx.Table or pd.DataFrame
        Input data.
    rows : int, list, slice, or None
        Row indices to select.
    cols : int, list, slice, or None
        Column indices to select.
    return_type : str, default 'q'
        'q' for pykx.Table, 'p' for pandas DataFrame.
        
    Returns
    -------
    pykx.Table or pd.DataFrame
        Subset of the inputs.
    """
    table = _ensure_q_table(df)

    count = kx.q("count", table).py()
    all_cols = kx.q("cols", table).py()

    # Track whether we can use the fast sublist path for contiguous row slices
    _use_sublist = False
    _slice_start = 0
    _slice_count = 0

    if rows is None:
        row_indices = None
    elif isinstance(rows, int):
        q_rows = rows
        if q_rows < 0: q_rows += count
        row_indices = [q_rows]
    elif isinstance(rows, slice):
        start, stop, step = rows.indices(count)
        if step == 1:
            _use_sublist = True
            _slice_start = start
            _slice_count = stop - start
            row_indices = None  # Not needed — sublist handles it
        else:
            row_indices = list(range(start, stop, step))
    else:
        row_indices = list(rows)
        row_indices = [r + count if r < 0 else r for r in row_indices]

    if cols is None:
        target_cols = None
    else:
        if isinstance(cols, int):
            target_cols = [all_cols[cols]]
        elif isinstance(cols, slice):
            target_cols = [all_cols[i] for i in range(*cols.indices(len(all_cols)))]
        else:
            target_cols = [all_cols[i] for i in cols]

    if not _use_sublist and row_indices is None and target_cols is None:
        return _handle_return(table, return_type)

    # Fast path: contiguous row slice via q's sublist (no Python list overhead)
    if _use_sublist:
        sublist_args = kx.LongVector([_slice_start, _slice_count])
        if target_cols is not None:
            syms = kx.SymbolVector(target_cols)
            cols_dict = kx.q('!', syms, syms)
            q_res = kx.q('{?[sublist[y;x];();0b;z]}', table, sublist_args, cols_dict)
        else:
            q_res = kx.q('{sublist[y;x]}', table, sublist_args)
    elif row_indices is not None and target_cols is not None:
        q_query = '{?[x y;();0b;z]}'
        syms = kx.SymbolVector(target_cols)
        cols_dict = kx.q('!', syms, syms)
        q_res = kx.q(q_query, table, kx.LongVector(row_indices), cols_dict)

    elif row_indices is not None:
        q_query = '{x y}'
        q_res = kx.q(q_query, table, kx.LongVector(row_indices))

    elif target_cols is not None:
        q_query = '{?[x;();0b;y]}'
        syms = kx.SymbolVector(target_cols)
        cols_dict = kx.q('!', syms, syms)
        q_res = kx.q(q_query, table, cols_dict)

    else:
        q_res = table

    return _handle_return(q_res, return_type)