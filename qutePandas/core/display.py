import pykx as kx
import pandas as pd
import builtins

def py(obj):
    """
    Converts a PyKX object to its Python equivalent.

    Parameters
    ----------
    obj : pykx.K
        The PyKX object to convert.

    Returns
    -------
    any
        The Python equivalent of the PyKX object.
    """
    try:
        return obj.py()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to Python: {e}")

def np(obj):
    """
    Converts a PyKX object to a NumPy array.

    Parameters
    ----------
    obj : pykx.K
        The PyKX object to convert.

    Returns
    -------
    numpy.ndarray
        The NumPy array equivalent.
    """
    try:
        return obj.np()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to NumPy: {e}")

def pd(obj):
    """
    Converts a PyKX object to a Pandas DataFrame or Series.

    Parameters
    ----------
    obj : pykx.K
        The PyKX object to convert.

    Returns
    -------
    pandas.DataFrame or pandas.Series
        The Pandas equivalent.
    """
    try:
        return obj.pd()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to Pandas: {e}")

def pa(obj):
    """
    Converts a PyKX object to a PyArrow Table.

    Parameters
    ----------
    obj : pykx.K
        The PyKX object to convert.

    Returns
    -------
    pyarrow.Table
        The PyArrow equivalent.
    """
    try:
        return obj.pa()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to PyArrow: {e}")

def pt(obj):
    """
    Converts a PyKX object to a PyTorch Tensor.

    Parameters
    ----------
    obj : pykx.K
        The PyKX object to convert.

    Returns
    -------
    torch.Tensor
        The PyTorch equivalent.
    """
    try:
        return obj.pt()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to PyTorch: {e}")

def print(obj, head=None, tail=None):
    """
    Prints a PyKX table in a formatted ASCII box.

    Parameters
    ----------
    obj : pykx.Table or pykx.KeyedTable
        The table to print.
    head : int, optional
        Number of rows to show from the beginning.
    tail : int, optional
        Number of rows to show from the end.
    """
    try:
        if isinstance(obj, (kx.Table, kx.KeyedTable)):
            if head is not None:
                table = kx.q('{[t;n] n sublist t}', obj, head)
            elif tail is not None:
                table = kx.q('{[t;n] neg[n] sublist t}', obj, tail)
            else:
                table = obj
            
            cols = kx.q('cols', table).py()
            if len(cols) == 0:
                builtins.print("Empty table")
                return
            
            rows_data = []
            for col in cols:
                col_data = kx.q('{[t;c] t[c]}', table, col).py()
                rows_data.append(col_data)
            
            num_rows = len(rows_data[0]) if rows_data else 0
            
            col_widths = []
            for i, col in enumerate(cols):
                max_width = len(str(col))
                for j in range(num_rows):
                    val_width = len(str(rows_data[i][j]))
                    max_width = max(max_width, val_width)
                col_widths.append(max_width)
            
            def format_row(values):
                parts = []
                for val, width in zip(values, col_widths):
                    parts.append(str(val).ljust(width))
                return "│ " + " │ ".join(parts) + " │"
            
            total_width = sum(col_widths) + 3 * len(cols) + 1
            top_border = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
            mid_border = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
            bot_border = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
            
            builtins.print(top_border)
            builtins.print(format_row(cols))
            builtins.print(mid_border)
            
            for row_idx in range(num_rows):
                row_values = [rows_data[col_idx][row_idx] for col_idx in range(len(cols))]
                builtins.print(format_row(row_values))
            
            builtins.print(bot_border)
        else:
            raise ValueError("Input must be a pykx Table or KeyedTable")
    except Exception as e:
        raise RuntimeError(f"Failed to print table: {e}")