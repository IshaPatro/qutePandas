"""
Display and conversion functions for qutePandas.

This module provides functions to convert PyKX objects to various Pythonic types.
Requires kdb+ and pykx to be properly installed and configured.
"""

import pykx as kx
import pandas as pd


def py(obj):
    """
    Convert a PyKX object to Python.
    
    Parameters
    ----------
    obj : PyKX object
        Input PyKX object to convert.
        
    Returns
    -------
    Python object
        Converted Python representation.
    """
    try:
        return obj.py()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to Python: {e}")


def np(obj):
    """
    Convert a PyKX object to NumPy.
    
    Parameters
    ----------
    obj : PyKX object
        Input PyKX object to convert.
        
    Returns
    -------
    numpy.ndarray
        Converted NumPy representation.
    """
    try:
        return obj.np()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to NumPy: {e}")


def pd(obj):
    """
    Convert a PyKX object to Pandas.
    
    Parameters
    ----------
    obj : PyKX object
        Input PyKX object to convert.
        
    Returns
    -------
    pandas.DataFrame or pandas.Series
        Converted Pandas representation.
    """
    try:
        return obj.pd()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to Pandas: {e}")


def pa(obj):
    """
    Convert a PyKX object to PyArrow.
    
    Parameters
    ----------
    obj : PyKX object
        Input PyKX object to convert.
        
    Returns
    -------
    pyarrow object
        Converted PyArrow representation.
    """
    try:
        return obj.pa()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to PyArrow: {e}")


def pt(obj):
    """
    Convert a PyKX object to PyTorch (Beta).
    
    Parameters
    ----------
    obj : PyKX object
        Input PyKX object to convert.
        
    Returns
    -------
    torch.Tensor
        Converted PyTorch representation.
    """
    try:
        return obj.pt()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PyKX object to PyTorch: {e}")