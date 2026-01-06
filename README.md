# qutePandas

A pandas-like library for q/kdb+ that replicates core pandas functionality with performance benchmarking capabilities.

## 📋 Overview

qutePandas is a Python library that provides pandas-like functionality while maintaining compatibility with q/kdb+ systems. Each function is implemented as a standalone module with comprehensive docstrings and performance benchmarking against pandas equivalents.

## 🏗️ Project Architecture

### How Pandas Modules Are Created

This project follows a modular architecture similar to pandas itself:

```
qutePandas/
├── __init__.py              # Main package entry point
├── utils.py                 # Utilities for dataset generation and benchmarking
├── cleaning/                # Data cleaning operations
│   ├── __init__.py         # Module exports
│   ├── drop_nulls.py       # Remove null rows
│   ├── drop_nulls_col.py   # Remove nulls from specific column
│   ├── fill_null.py        # Fill null values
│   └── remove_duplicates.py # Remove duplicate rows
├── transformation/          # Data transformation operations
│   ├── __init__.py
│   ├── rename.py           # Rename columns
│   ├── cast.py             # Type casting
│   └── drop_col.py         # Drop columns
├── joining/                 # Data joining operations
│   ├── __init__.py
│   ├── merge_left.py       # Left join
│   └── merge_inner.py      # Inner join
├── grouping/                # Grouping and aggregation
│   ├── __init__.py
│   ├── groupby_sum.py      # Group by and sum
│   └── groupby_avg.py      # Group by and average
├── io/                      # Input/Output operations
│   ├── __init__.py
│   ├── to_csv.py           # Export to CSV
│   └── from_csv.py         # Import from CSV
└── apply/                   # Apply functions
    ├── __init__.py
    ├── apply.py            # Apply function to rows/columns
    └── apply_col.py        # Apply function to specific column
```

### Function Design Principles

Each function follows these principles:

1. **Single Responsibility**: One function per file
2. **Comprehensive Docstrings**: Complete documentation with parameters, returns, and examples
3. **No Comments**: Only docstrings are used for documentation
4. **Performance Benchmarking**: All functions are benchmarked against pandas equivalents
5. **Pandas Compatibility**: Functions accept and return pandas DataFrames

### Example Function Structure

```python
def drop_nulls(df):
    """
    Removes all rows from the DataFrame that contain null values in any column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.DataFrame
        DataFrame with null rows removed.

    Example
    -------
    >>> import pandas as pd
    >>> from qutePandas.cleaning.drop_nulls import drop_nulls
    >>> df = pd.DataFrame({'a': [1, 2, None, 4], 'b': ['x', 'y', None, 'z']})
    >>> drop_nulls(df)
       a  b
    0  1  x
    1  2  y
    3  4  z
    """
    return df.dropna()
```

## 🚀 Installation

### Quick Start

```bash
# Create virtual environment
python -m venv venvQutePandas
source venvQutePandas/bin/activate  # On Windows: venvQutePandas\Scripts\activate

# Install qutePandas in development mode
pip install -e .
```

### Complete Setup Guide

For detailed installation instructions including PyKX setup, kdb+ configuration, and license management, see our comprehensive installation guide:

**📖 [PyKX Installation Guide](PYKX_INSTALLATION.md)**

The installation guide covers:
- ✅ kdb+ installation (free and commercial versions)
- ✅ PyKX setup and configuration  
- ✅ License management (including base64 license setup)
- ✅ Environment variable configuration
- ✅ Troubleshooting common issues
- ✅ Platform-specific instructions (Windows, macOS, Linux)

### Optional: Jupyter Kernel

```bash
python install_kernel.py
```

## 🧪 Testing and Benchmarking

### Running All Tests

```bash
# Run all functional tests and performance benchmarks
cd tests
python run_all_tests.py
```

### Individual Test Categories

```bash
# Functional tests only
python test_cleaning.py
python test_transformation.py
python test_joining.py
python test_grouping.py
python test_io.py
python test_apply.py

# Performance benchmarks
python test_performance.py
```

### Performance Benchmarking

The library includes comprehensive performance benchmarking that compares qutePandas functions against pandas equivalents:

```python
from qutePandas.utils import generate_large_dataset, compare_performance
from qutePandas.cleaning import drop_nulls

# Generate test data
df = generate_large_dataset(50000, 8, 0.1)

# Compare performance
results = compare_performance(df.dropna, drop_nulls, df)
print(f"Speedup: {results['speedup']:.2f}x")
```

## 📊 Features

### Data Cleaning
- **drop_nulls**: Remove rows with any null values
- **drop_nulls_col**: Remove rows with nulls in specific column
- **fill_null**: Fill null values with specified value
- **remove_duplicates**: Remove duplicate rows

### Data Transformation
- **rename**: Rename columns
- **cast**: Convert column data types
- **drop_col**: Remove columns

### Data Joining
- **merge_left**: Left join two DataFrames
- **merge_inner**: Inner join two DataFrames

### Grouping Operations
- **groupby_sum**: Group by columns and sum
- **groupby_avg**: Group by columns and average

### I/O Operations
- **to_csv**: Export DataFrame to CSV
- **from_csv**: Import DataFrame from CSV

### Apply Functions
- **apply**: Apply function to rows or columns
- **apply_col**: Apply function to specific column

### Utilities
- **generate_large_dataset**: Create large datasets for testing
- **compare_performance**: Benchmark functions against pandas
- **benchmark_all_functions**: Run comprehensive benchmarks

## 💻 Usage Examples

### Basic Usage

```python
import pandas as pd
import qutePandas

# Create sample data
df = pd.DataFrame({
    'a': [1, 2, None, 4],
    'b': ['x', 'y', None, 'z']
})

# Use qutePandas functions
clean_df = qutePandas.drop_nulls(df)
filled_df = qutePandas.fill_null(df, 'a', 0)
renamed_df = qutePandas.rename(df, {'a': 'column_a'})
```

### Performance Benchmarking

```python
from qutePandas.utils import generate_large_dataset, compare_performance
from qutePandas.cleaning import drop_nulls

# Generate large dataset
df = generate_large_dataset(100000, 10, 0.15)

# Benchmark against pandas
results = compare_performance(df.dropna, drop_nulls, df)
print(f"qutePandas is {results['speedup']:.2f}x faster than pandas")
```

### Comprehensive Benchmarking

```python
from qutePandas.utils import benchmark_all_functions

# Run all benchmarks
results = benchmark_all_functions()
```

## 🔧 Development

### Adding New Functions

1. Create a new file in the appropriate module directory
2. Implement the function with comprehensive docstring
3. Add the function to the module's `__init__.py`
4. Create corresponding tests in the `tests/` directory
5. Add performance benchmarks

### Code Standards

- **Docstrings**: Use NumPy-style docstrings for all functions
- **No Comments**: Only docstrings are allowed, no inline comments
- **Type Hints**: Use type hints where appropriate
- **Testing**: All functions must have both functional and performance tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your function following the established patterns
4. Include comprehensive tests and benchmarks
5. Submit a pull request

## 📈 Performance Philosophy

qutePandas is designed with performance in mind:

- **Benchmarking First**: Every function is benchmarked against pandas
- **Optimization Focus**: Functions are optimized for large datasets
- **Transparency**: Performance results are clearly reported
- **Continuous Improvement**: Regular benchmarking identifies optimization opportunities

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **"No module named 'qutePandas'"**:
   - Ensure you're in the correct virtual environment
   - Run `pip install -e .` in the project root

2. **PyKX/kdb+ Integration Issues**:
   - See our comprehensive **[PyKX Installation Guide](PYKX_INSTALLATION.md)** for detailed troubleshooting
   - Verify `QLIC` environment variable: `echo $QLIC`
   - Check license file exists: `ls -la $QLIC/kc.lic`
   - Verify PyKX installation: `python -c "import pykx; print('PyKX OK')"`

3. **Performance Test Failures**:
   - Ensure sufficient memory for large datasets
   - Check that all dependencies are installed
   - Verify pandas and numpy versions are compatible

### Getting Help

- **Installation Issues**: Check [PyKX Installation Guide](PYKX_INSTALLATION.md)
- **Usage Examples**: Review test files and function docstrings
- **Performance**: Run `python test_performance.py` to see benchmark results
- **Debug Information**: Use the debug script in the installation guide 