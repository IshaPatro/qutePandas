import pykx as kx
import pandas as pd
from ..utils import _ensure_q_table, _handle_return


def merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, return_type="q"):
    """
    Merge DataFrame or pykx.Table objects with a database-style join.

    Parameters
    ----------
    left : pandas.DataFrame or pykx.Table
        Left object.
    right : pandas.DataFrame or pykx.Table
        Right object.
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        Type of merge to be performed.
    on : label or list
        Column or index level names to join on. These must be found in both DataFrames.
    left_on : label or list
        Column or index level names to join on in the left DataFrame.
    right_on : label or list
        Column or index level names to join on in the right DataFrame.
    left_index : bool, default False
        Use the index from the left DataFrame as the join key(s). (Currently not fully supported)
    right_index : bool, default False
        Use the index from the right DataFrame as the join key(s). (Currently not fully supported)
    sort : bool, default False
        Sort the join keys lexicographically in the result DataFrame. (Currently not fully supported)
    return_type : str, default 'q'
        Desired return type ('p' or 'q').

    Returns
    -------
    pandas.DataFrame or pykx.Table
        Merged object.
    """
    try:
        q_left = _ensure_q_table(left)
        q_right = _ensure_q_table(right)

        if on is None and left_on is None and right_on is None:
            left_cols = set(kx.q("cols", q_left).py())
            right_cols = set(kx.q("cols", q_right).py())
            common = list(left_cols.intersection(right_cols))
            if not common:
                raise ValueError("No common columns found and no join keys specified.")
            on = common

        l_keys = on if left_on is None else left_on
        r_keys = on if right_on is None else right_on

        if isinstance(l_keys, str):
            l_keys = [l_keys]
        if isinstance(r_keys, str):
            r_keys = [r_keys]

        if l_keys != r_keys:
            update_clauses = []
            for lk, rk in zip(l_keys, r_keys):
                if lk != rk:
                    update_clauses.append(f"{lk}:{rk}")
            
            if update_clauses:
                update_str = ",".join(update_clauses)
                q_right = kx.q(f"{{update {update_str} from x}}", q_right)
            
            r_keys = l_keys

        key_cols = "`" + "`".join(l_keys)

        if how == 'inner':
            keyed_right = kx.q(f'{{ {key_cols} xkey x }}', q_right)
            result = kx.q("{x ij y}", q_left, keyed_right)
        elif how == 'left':
            keyed_right = kx.q(f'{{ {key_cols} xkey x }}', q_right)
            result = kx.q("{x lj y}", q_left, keyed_right)
        elif how == 'right':
            keyed_left = kx.q(f'{{ {key_cols} xkey x }}', q_left)
            result = kx.q("{x lj y}", q_right, keyed_left)
            left_all_cols = kx.q("cols", q_left).py()
            right_all_cols = kx.q("cols", q_right).py()
            target_cols = "`" + "`".join(left_all_cols + [c for c in right_all_cols if c not in left_all_cols])
            result = kx.q(f"{{ {target_cols} xcols x }}", result)
        elif how == 'outer':
            keyed_left = kx.q(f'{{ {key_cols} xkey x }}', q_left)
            keyed_right = kx.q(f'{{ {key_cols} xkey x }}', q_right)
            result = kx.q("{0! x uj y}", keyed_left, keyed_right)
        else:
            raise ValueError(f"Invalid how: {how}. Must be one of 'left', 'right', 'outer', 'inner'.")

        return _handle_return(result, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to perform {how} join: {e}")
