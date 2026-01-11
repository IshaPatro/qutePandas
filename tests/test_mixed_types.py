
import os
import sys
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
import qutePandas as qpd
import pandas as pd
import numpy as np
import pykx as kx
from test_utils import verify_correctness

# Setup License
local_lic = os.path.abspath('../kdb_lic')
if os.path.exists(local_lic): os.environ['QLIC'] = local_lic
qpd.connect()

print("Setup Complete")

# Define Data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', None],
    'age': [25, 30, 35, 40, None],
    'gender': ['F', 'M', 'M', 'M', None],
    'date_of_birth': [pd.Timestamp('1998-01-01'), pd.Timestamp('1993-02-15'), 
                      pd.Timestamp('1988-06-20'), pd.Timestamp('1983-11-05'), pd.NaT]
}
df = pd.DataFrame(data)
q_df = qpd.DataFrame(df)

print("DataFrame Created")

# Test 1: dropna
print("\nTest: dropna")
pd_res = df.dropna()
q_res = qpd.dropna(q_df, return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 2: dropna_col
print("\nTest: dropna_col (subset=['age'])")
pd_res = df.dropna(subset=['age'])
q_res = qpd.dropna_col(q_df, 'age', return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 3: fillna
print("\nTest: fillna (age -> 0)")
pd_res = df.fillna({'age': 0})
q_res = qpd.fillna(q_df, 'age', 0, return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 4: rename
print("\nTest: rename (name -> full_name)")
pd_res = df.rename(columns={'name': 'full_name'})
q_res = qpd.rename(q_df, {'name': 'full_name'}, return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 5: cast
print("\nTest: cast (age -> float)")
pd_res = df.copy()
pd_res['age'] = pd_res['age'].astype(float)
q_res_table = qpd.cast(q_df, 'age', 'float', return_type='q')
q_res = q_res_table.pd()
# Normalization in verify_correctness handles float/int nuances often, 
# but let's check explicit column mainly.
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 6: drop_col
print("\nTest: drop_col (gender)")
pd_res = df.drop(columns=['gender'])
q_res = qpd.drop_col(q_df, 'gender', return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 7: groupby_sum 
print("\nTest: groupby_sum (gender, age)") 
# qutePandas returns a DataFrame with the group column and aggregated column
pd_res = df.groupby('gender', dropna=False)['age'].sum()
q_res = qpd.groupby_sum(q_df, 'gender', 'age', return_type='p').set_index('gender')['age']
assert verify_correctness(pd_res, q_res) 
print("Passed")


# Test 8: groupby_avg 
print("\nTest: groupby_avg (gender, age)")
pd_res = df.groupby('gender', dropna=False)['age'].mean()
q_res = qpd.groupby_avg(q_df, 'gender', 'age', return_type='p').set_index('gender')['age']
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 9: apply (builtin)
# Hard to find a builtin numeric row-wise op that works on strings, 
# so let's subset first
print("\nTest: apply (sum numeric subset)")
df_num = df[['age']]
q_num = kx.toq(df_num)
pd_res = df_num.sum(axis=1)
q_res = qpd.apply(q_num, 'sum', axis=1, return_type='p')
assert verify_correctness(pd_res, q_res)
print("Passed")

# Test 10: dtypes
print("\nTest: dtypes")
pd_res = df.dtypes
q_res = qpd.dtypes(q_df, return_type='p')
# q_res is a dataframe describing types, pd_res is a Series.
# We just check it runs and returns a dataframe
assert isinstance(q_res, pd.DataFrame)
assert len(q_res) == 4
print("Passed")

print("\nAll Tests Passed!")
