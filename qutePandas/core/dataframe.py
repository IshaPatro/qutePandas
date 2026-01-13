import pykx as kx
import pandas as pd
import os
import atexit
from ..utils import _handle_return

os.environ['PYKX_ENFORCE_EMBEDDED_IMPORT'] = '0'

def DataFrame(data, columns=None):
    """
    Creates a qutePandas DataFrame (internal pykx Table).

    Parameters
    ----------
    data : array-like, dict, or pandas.DataFrame
        Data to be stored in the table.
    columns : list, optional
        Column names to use if data does not already have them.

    Returns
    -------
    pykx.Table
        The resulting kdb+ table.
    """
    try:
        if isinstance(data, pd.DataFrame):
            q_res = kx.toq(data)
        elif isinstance(data, (kx.Table, kx.KeyedTable)):
            q_res = data
        elif isinstance(data, dict):
            q_res = _dict_to_table(data)
        elif isinstance(data, list) and data and isinstance(data[0], list):
            q_res = _lists_to_table(data, columns)
        else:
            q_res = _data_to_table(data, columns)
        return _handle_return(q_res)
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table: {e}")


def _dict_to_table(data_dict):
    """
    Converts a dictionary to a kdb+ table.

    Parameters
    ----------
    data_dict : dict
        Dictionary to convert.

    Returns
    -------
    pykx.Table
        The resulting kdb+ table.
    """
    try:
        q_dict = kx.toq(data_dict)
        return kx.q("{flip x}", q_dict)
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table from dict: {e}")


def _lists_to_table(data_lists, columns=None):
    """
    Converts a list of lists to a kdb+ table.

    Parameters
    ----------
    data_lists : list of lists
        Data to convert.
    columns : list, optional
        Column names.

    Returns
    -------
    pykx.Table
        The resulting kdb+ table.
    """
    try:
        if not data_lists:
            return kx.q("([] )")
            
        if columns is None:
            columns = [f'col_{i}' for i in range(len(data_lists[0]))]

        transposed = list(zip(*data_lists))
        data_dict = {columns[i]: list(col_data) for i, col_data in enumerate(transposed)}
        q_dict = kx.toq(data_dict)
        return kx.q("{flip x}", q_dict)
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table from lists: {e}")


def _data_to_table(data, columns=None):
    """
    Converts generic data to a kdb+ table.

    Parameters
    ----------
    data : any
        Data to convert.
    columns : list, optional
        Column names.

    Returns
    -------
    pykx.Table
        The resulting kdb+ table.
    """
    try:
        if hasattr(data, '__iter__') and not isinstance(data, (str, dict)):
            data_list = list(data)
            if columns:
                data_dict = {col: [row[i] if hasattr(row, '__getitem__') else row for row in data_list] 
                           for i, col in enumerate(columns)}
                return _dict_to_table(data_dict)
            else:
                return kx.toq(pd.DataFrame({'data': data_list}))
        else:
            return kx.toq(pd.DataFrame({'data': [data]}))
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table from data: {e}")