import pykx as kx
import pandas as pd
import numpy as numpy
import time
import random
import string

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


def generate_large_dataset(rows=100000, cols=10, null_percentage=0.1):
    """
    Generates a large DataFrame with random values for performance testing.
    """
    numpy.random.seed(42)
    random.seed(42)
    
    data = {}
    
    for i in range(cols):
        col_name = f'col_{i}'
        
        if i % 4 == 0:
            data[col_name] = numpy.random.randint(1, 1000, rows)
        elif i % 4 == 1:
            data[col_name] = numpy.random.uniform(0, 100, rows)
        elif i % 4 == 2:
            data[col_name] = [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(rows)]
        else:
            data[col_name] = numpy.random.choice(['A', 'B', 'C', 'D'], rows)
    
    df = pd.DataFrame(data)
    
    if null_percentage > 0:
        for col in df.columns:
            null_indices = numpy.random.choice(df.index, size=int(rows * null_percentage), replace=False)
            df.loc[null_indices, col] = None
    
    return df

def compare_performance(pandas_func, qutepandas_func, data, iterations=3):
    """
    Compares performance between pandas and qutePandas functions.
    """
    pandas_times = []
    qutepandas_times = []
    
    for _ in range(iterations):
        data_copy = data.copy()
        
        start_time = time.time()
        try:
            pandas_result = pandas_func(data_copy)
        except TypeError:
            pandas_result = pandas_func()
        pandas_times.append(time.time() - start_time)
        
        data_copy = data.copy()
        start_time = time.time()
        qutepandas_result = qutepandas_func(data_copy)
        qutepandas_times.append(time.time() - start_time)
    
    pandas_avg = numpy.mean(pandas_times)
    qutepandas_avg = numpy.mean(qutepandas_times)
    
    try:
        q_as_pd = qutepandas_result.pd() if hasattr(qutepandas_result, 'pd') else qutepandas_result
        results_equal = pandas_result.equals(q_as_pd)
    except:
        results_equal = pandas_result.shape == qutepandas_result.shape
    
    speedup = pandas_avg / qutepandas_avg if qutepandas_avg > 0 else float('inf')
    
    return {
        'pandas_time': pandas_avg,
        'qutepandas_time': qutepandas_avg,
        'speedup': speedup,
        'results_equal': results_equal,
        'pandas_times': pandas_times,
        'qutepandas_times': qutepandas_times
    }

def benchmark_all_functions():
    """
    Runs comprehensive benchmarks for all qutePandas functions.
    """
    from qutePandas.cleaning import drop_nulls, drop_nulls_col, fill_null, remove_duplicates
    from qutePandas.transformation import rename, cast, drop_col
    from qutePandas.joining import merge_left, merge_inner
    from qutePandas.grouping import groupby_sum, groupby_avg
    from qutePandas.apply import apply, apply_col
    
    results = {}
    
    print("Running comprehensive benchmarks...")
    print("=" * 50)
    
    df = generate_large_dataset(50000, 8)
    
    print("Cleaning Functions:")
    results['cleaning'] = {}
    
    bench_result = compare_performance(df.dropna, drop_nulls, df)
    results['cleaning']['drop_nulls'] = bench_result
    print(f"  drop_nulls: {bench_result['speedup']:.2f}x speedup")
    
    col = df.columns[0]
    pandas_func = lambda data: data[data[col].notna()]
    bench_result = compare_performance(pandas_func, lambda data: drop_nulls_col(data, col), df)
    results['cleaning']['drop_nulls_col'] = bench_result
    print(f"  drop_nulls_col: {bench_result['speedup']:.2f}x speedup")
    
    return results