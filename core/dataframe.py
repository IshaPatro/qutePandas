"""
DataFrame creation functions for qutePandas.

This module provides functions to create DataFrames using kdb+/q backend.
Requires kdb+ and pykx to be properly installed and configured.
"""

import pykx as kx
import os
import atexit
from qutePandas.utils import _handle_return

os.environ['PYKX_ENFORCE_EMBEDDED_IMPORT'] = '0'
_q_server = None
_q_conn = None

def _get_q_connection():
    """Get or create a q connection for executing queries"""
    global _q_server, _q_conn
    if _q_conn is None or _q_server is None:
        try:
            _q_server = kx.util.start_q_subprocess(port=5054)
            _q_conn = kx.SyncQConnection(port=5054)
        except Exception as e:
            raise RuntimeError(f"Failed to establish q connection: {e}")
    return _q_conn

def _cleanup_q_connection():
    """Close the q connection and server when done"""
    global _q_server, _q_conn
    if _q_conn is not None:
        try:
            _q_conn.close()
        except:
            pass
        _q_conn = None
    if _q_server is not None:
        try:
            _q_server.kill()
        except:
            pass
        _q_server = None

atexit.register(_cleanup_q_connection)

def DataFrame(data, columns=None, return_type='q'):
    """
    Create DataFrame using kdb+ backend.
    
    Creates a kdb+ table from various data structures using pure q operations.
    
    Parameters
    ----------
    data : dict, list of lists, or other data structure
        Data to create DataFrame from.
    columns : list of str, optional
        Column names. If None and data is list of lists, defaults to auto-generated names.
    return_type : str, default 'q'
        Desired return type ('pandas' or 'q').
        
    Returns
    -------
    pandas.DataFrame or pykx.Table
        DataFrame created from kdb+ operations.
    """
    try:
        if isinstance(data, dict):
            q_res = _dict_to_table(data)
        elif isinstance(data, list) and data and isinstance(data[0], list):
            q_res = _lists_to_table(data, columns)
        else:
            q_res = _data_to_table(data, columns)
            
        return _handle_return(q_res, return_type)
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table: {e}")


def _dict_to_table(data_dict):
    try:
        q_dict = kx.toq(data_dict)
        result = kx.q("{flip x}", q_dict)
        return result
        
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table from dict: {e}")


def _lists_to_table(data_lists, columns=None):
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
    try:
        if hasattr(data, '__iter__') and not isinstance(data, (str, dict)):
            data_list = list(data)
            if columns:
                data_dict = {col: [row[i] if hasattr(row, '__getitem__') else row for row in data_list] 
                           for i, col in enumerate(columns)}
                return _dict_to_table(data_dict)
            else:
                conn = _get_q_connection()
                result = conn(f"([] data:{' '.join(str(x) for x in data_list)})")
                return result
        else:
            conn = _get_q_connection()
            result = conn(f"([] data:enlist {data})")
            return result
    except Exception as e:
        raise RuntimeError(f"Failed to create kdb+ table from data: {e}")
 