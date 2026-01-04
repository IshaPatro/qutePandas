import pykx as kx
import pandas as pd
import numpy as numpy

def _ensure_q_table(data):
    """
    Ensures input data is a kdb+ table.
    """
    if isinstance(data, (kx.Table, kx.KeyedTable)):
        return data
    elif isinstance(data, pd.DataFrame):
        return kx.toq(data)
    else:
        raise ValueError("Input must be a pandas DataFrame or pykx Table")

def _handle_return(q_object, return_type='q'):
    """
    Handles return value based on specified return type.
    """
    if return_type == 'pandas':
        return q_object.pd()
    elif return_type == 'q':
        return q_object
    else:
        raise ValueError(f"Invalid return_type: {return_type}. Must be 'pandas' or 'q'.")