
import numpy as np
import pandas as pd
import pykx as kx
import time
import gc
import random
import string

def generate_large_dataset(rows=10_000_000, cols=20, null_percentage=0.1):
    np.random.seed(42)
    random.seed(42)
    data = {}
    for i in range(cols):
        col_name = f'col_{i}'
        if i % 5 == 0: data[col_name] = np.random.randint(1, 1000, rows)
        elif i % 5 == 1: data[col_name] = np.random.uniform(0, 100, rows)
        elif i % 5 == 2:
            pool = [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(100)]
            data[col_name] = np.random.choice(pool, rows)
        elif i % 5 == 3: data[col_name] = np.random.choice(['A', 'B', 'C', 'D'], rows)
        else: data[col_name] = np.random.randn(rows)
    df = pd.DataFrame(data)
    if null_percentage > 0:
        for col in df.columns:
            mask = np.random.rand(rows) < null_percentage
            if df[col].dtype.kind in 'if': df.loc[mask, col] = np.nan
            else: df.loc[mask, col] = None
    return df

def benchmark_operation(func, iterations=5, warmup=True):
    if warmup:
        try: func()
        except: pass 
    times = []
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return {'mean': np.mean(times)}

def verify_correctness(p, q):
    if hasattr(q, 'pd'): q = q.pd()
    if p is None or q is None: return p == q
    
    def _norm(obj):
        if not isinstance(obj, (pd.Series, pd.DataFrame)): return obj
        res = obj.copy()
        if isinstance(res, pd.Series):
            idx = [str(x) if (x is not None and str(x) != 'nan' and str(x) != '') else 'nan_ext' for x in res.index]
            res.index = idx
            res = res.sort_index()
            if res.dtype.name in ['Int64', 'Int32', 'Float64', 'boolean', 'float64', 'int64']:
                res = pd.Series(res.to_numpy(dtype=float, na_value=np.nan), index=res.index)
            elif res.dtype == 'object':
                res = res.replace("", None).fillna(np.nan)
            return res.reset_index(drop=True)
        else:
            for c in res.columns:
                if res[c].dtype.name in ['Int64', 'Int32', 'Float64', 'boolean', 'float64', 'int64']:
                    res[c] = res[c].to_numpy(dtype=float, na_value=np.nan)
                elif res[c].dtype == 'object':
                    res[c] = res[c].replace("", None).fillna(np.nan)
            return res.reset_index(drop=True)
            
    p_n, q_n = _norm(p), _norm(q)
    try:
        if isinstance(p_n, pd.Series): 
            pd.testing.assert_series_equal(p_n, q_n, check_dtype=False, atol=1e-5)
        else: 
            pd.testing.assert_frame_equal(p_n, q_n, check_dtype=False, check_like=True, atol=1e-5)
        return True
    except: 
        return False

def calculate_speedup(pd_stats, q_stats):
    print("  Speedup:", pd_stats['mean'] / q_stats['mean'])
