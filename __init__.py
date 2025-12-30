"""
qutePandas - A pandas-like library for q/kdb+
"""

from .core.dataframe import DataFrame
from .core.connection import connect, get_license_info, install_license
from .core.display import py, np, pd, pa, pt

from .cleaning.drop_nulls import drop_nulls
from .cleaning.drop_nulls_col import drop_nulls_col
from .cleaning.fill_null import fill_null
from .cleaning.remove_duplicates import remove_duplicates

from .transformation.cast import cast
from .transformation.drop_col import drop_col
from .transformation.rename import rename

from .joining.merge_left import merge_left
from .joining.merge_inner import merge_inner

from .grouping.groupby_sum import groupby_sum
from .grouping.groupby_avg import groupby_avg

from .io.to_csv import to_csv
from .io.from_csv import from_csv

from .apply.apply import apply
from .apply.apply_col import apply_col

from .utils import generate_large_dataset, compare_performance, benchmark_all_functions

__version__ = "1.0.0"
