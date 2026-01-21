"""
iloc - Integer-location based indexing for qutePandas.

Performance Optimization Notes:
------------------------------
For contiguous row slices (step=1), this module uses kdb+'s native `sublist`
function instead of enumerating indices. This provides O(1) slicing performance
comparable to numpy/pandas, avoiding the overhead of creating large Python lists
of indices for operations like `iloc[0:1000000]`.

Previous approach: slice[0:N] -> list(range(N)) -> pass N indices to q
Optimized approach: slice[0:N] -> sublist[(start;count);table] (zero-copy view)
"""

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
    
    # Track if we can use optimized slice path
    use_slice_optimization = False
    slice_start = 0
    slice_count = 0

    if rows is None:
        row_indices = None
    elif isinstance(rows, int):
        q_rows = rows
        if q_rows < 0: q_rows += count
        row_indices = [q_rows]
    elif isinstance(rows, slice):
        start, stop, step = rows.indices(count)
        if step == 1:
            # Use optimized path with q's native sublist
            use_slice_optimization = True
            slice_start = start
            slice_count = stop - start
            row_indices = None  # Not needed for optimized path
        else:
            # Fall back to enumeration only for non-unit steps
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
            
    if row_indices is None and target_cols is None and not use_slice_optimization:
        return _handle_return(table, return_type)

    # Optimized path for contiguous slices (step=1)
    if use_slice_optimization:
        if target_cols is not None:
            # Slice rows and select columns
            syms = kx.SymbolVector(target_cols)
            cols_dict = kx.q('!', syms, syms)
            q_res = kx.q('{?[sublist[x;y];();0b;z]}', [slice_start, slice_count], table, cols_dict)
        else:
            # Just slice rows using sublist (O(1) operation)
            q_res = kx.q('{sublist[x;y]}', [slice_start, slice_count], table)
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
