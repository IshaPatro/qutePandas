# Contributing to qutePandas

Thank you for your interest in contributing to qutePandas! I welcome contributions from the community to help make this library better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation Requirements](#documentation-requirements)
- [Benchmarking Requirements](#benchmarking-requirements)
- [Code Style](#code-style)
- [Questions and Support](#questions-and-support)

---

## Code of Conduct

I am committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

---

## Getting Started

Before contributing, please:

1. **Check existing issues** to see if your idea or bug has already been reported
2. **Open an issue** to discuss major changes before starting work
3. **Fork the repository** and create a feature branch for your work

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- kdb+ license (or use PyKX unlicensed mode for development)
- Git

### Setup Instructions

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/qutePandas.git
   cd qutePandas
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv_dev
   source venv_dev/bin/activate  # macOS/Linux
   # OR
   venv_dev\Scripts\activate     # Windows
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Configure PyKX** (choose one option):
   
   **Option A: Unlicensed Mode (Recommended for Development)**
   ```bash
   export PYKX_UNLICENSED=true
   ```
   
   **Option B: Commercial License**
   ```bash
   # Place kc.lic in one of these locations:
   mkdir -p kdb_lic
   cp /path/to/your/kc.lic kdb_lic/
   ```

5. **Verify setup**:
   ```bash
   python tests/test_pykx_setup.py
   ```

For detailed setup instructions, see [tests/README.md](tests/README.md).

---

## Contribution Guidelines

### What to Contribute

I welcome contributions in the following areas:

- **New Functions**: Add pandas-like operations that leverage kdb+/q performance
- **Bug Fixes**: Fix issues in existing functionality
- **Performance Improvements**: Optimize existing q queries for better performance
- **Documentation**: Improve docs, examples, or tutorials
- **Tests**: Add test coverage for existing or new features

### What NOT to Contribute

- **Features that don't align with the pandas API**: This library aims to provide a pandas-like interface
- **Changes that break backward compatibility**: Discuss breaking changes in an issue first
- **Implementations NOT using q queries**: All underlying computation MUST be done using kdb+/q queries, not Python/pandas operations
- **Functions without dual return type support**: Every function MUST support both `return_type='p'` (pandas) and `return_type='q'` (PyKX Table)
- **Code that uses pandas as intermediate data structure**: Pandas should only be used for input/output conversion, never for computation

---

## Pull Request Process

### Before Submitting a PR

Ensure your contribution meets ALL of the following requirements:

1. ✅ **Function Description**: Clearly state what function(s) you are adding/modifying
2. ✅ **Q-Based Implementation**: All computation MUST use kdb+/q queries (no pandas/numpy operations)
3. ✅ **Dual Return Type Support**: Function MUST support both `return_type='p'` and `return_type='q'`
4. ✅ **Documentation**: Add comprehensive docstrings and update relevant docs
5. ✅ **Tests**: Include test cases that verify correctness for BOTH return types
6. ✅ **Benchmarks**: Provide performance benchmarks comparing to pandas
7. ✅ **PR Description**: Mention all of the above in your pull request

### PR Template

When creating a pull request, use this template:

```markdown
## Description

Brief description of what this PR does.

## Function(s) Added/Modified

- `function_name_1`: Brief description
- `function_name_2`: Brief description

## Changes Made

- [ ] Added new function(s) to `qutePandas/[module]/[file].py`
- [ ] Implementation uses kdb+/q queries (NOT pandas/numpy operations)
- [ ] Function supports BOTH `return_type='p'` and `return_type='q'`
- [ ] Added comprehensive docstrings following project conventions
- [ ] Updated documentation in `docs/` (if applicable)
- [ ] Added test cases to verify correctness
- [ ] Added benchmarks comparing performance to pandas
- [ ] All tests pass (`python tests/test_pykx_setup.py`)

## Documentation

### Docstring Example

**IMPORTANT**: Your function MUST support both return types:
```python
def my_new_function(table, param1, return_type='p'):
    """
    Brief one-line description.
    
    Detailed description of what the function does and how it works.
    This implementation uses kdb+/q queries for high-performance computation.
    
    Parameters
    ----------
    table : pykx.Table
        Description of parameter
    param1 : type
        Description of parameter
    return_type : str, default 'p'
        Return type: 'p' for pandas DataFrame, 'q' for PyKX Table.
    
    Returns
    -------
    pd.DataFrame or pykx.Table
        Description of return value. Return type depends on `return_type` parameter.
    
    Examples
    --------
    >>> import qutePandas as qpd
    >>> df = qpd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    >>> 
    >>> # Return as pandas DataFrame
    >>> result_p = qpd.my_new_function(df, param1='value', return_type='p')
    >>> 
    >>> # Return as PyKX Table
    >>> result_q = qpd.my_new_function(df, param1='value', return_type='q')
    """
```

### Documentation Files Updated
- [ ] `docs/usage.html` (if adding user-facing functionality)
- [ ] `docs/api.html` (if adding new API methods)
- [ ] `README.md` (if changing core functionality)

## Testing

### Test Cases Added

Add your test cases to the appropriate notebook:

**For Benchmarking** (performance tests):
- Add to `tests/benchmark_tests.ipynb`
- Include tests with multiple dataset sizes (100K, 1M, 10M rows)
- Compare qutePandas performance vs pandas

**For Edge Cases** (correctness tests):
- Add to `tests/edge_cases.ipynb`
- Test edge cases: empty DataFrames, single row/column, null values, etc.
- Test both `return_type='p'` and `return_type='q'`

### Checklist
- [ ] Added benchmark tests to `tests/benchmark_tests.ipynb`
- [ ] Added edge case tests to `tests/edge_cases.ipynb`
- [ ] Tested with `return_type='p'` (returns pandas DataFrame)
- [ ] Tested with `return_type='q'` (returns PyKX Table)
- [ ] Both return types produce equivalent results to pandas
- [ ] All tests pass successfully

## Additional Notes

Any additional context, design decisions, or trade-offs made.

## Checklist

- [ ] My code follows the project's code style
- [ ] I have added comprehensive docstrings
- [ ] I have updated relevant documentation
- [ ] I have added tests that prove my fix/feature works
- [ ] I have added benchmarks comparing to pandas
- [ ] All tests pass locally
- [ ] I have mentioned all changes in this PR description
```

---

## Testing Requirements

All contributions MUST include tests in the existing test notebooks.

### Where to Add Tests

**Benchmark Tests** → `tests/benchmark_tests.ipynb`
- Performance comparisons with pandas
- Multiple dataset sizes (100K, 1M, 10M rows)
- Time and memory measurements

**Edge Case Tests** → `tests/edge_cases.ipynb`
- Correctness verification
- Edge cases (empty DataFrames, nulls, single row/column, etc.)
- Both return types (`return_type='p'` and `return_type='q'`)

### Critical Requirement: Test Both Return Types

**Every function MUST be tested with BOTH `return_type='p'` and `return_type='q'`**

### Example Test Structure

Add a new cell to the appropriate notebook:

```python
# Test: your_function_name
import pandas as pd
import qutePandas as qpd
import pykx as kx

# Create test data
pdf = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
qdf = qpd.DataFrame(pdf)

# Test correctness vs pandas
pandas_result = pdf.your_pandas_equivalent()
qutepandas_result = qpd.your_function(qdf, return_type='p')
assert pandas_result.equals(qutepandas_result), "Results don't match!"

# Test both return types
result_p = qpd.your_function(qdf, return_type='p')
result_q = qpd.your_function(qdf, return_type='q')
assert isinstance(result_p, pd.DataFrame), "return_type='p' must return pandas DataFrame"
assert isinstance(result_q, kx.Table), "return_type='q' must return PyKX Table"
assert result_p.equals(result_q.pd()), "Both return types must produce same results"

print("✅ All tests passed!")
```

### What to Test

**Edge Cases** (add to `tests/edge_cases.ipynb`):
- Empty DataFrames
- Single row/column DataFrames
- DataFrames with null values
- Large datasets (1M+ rows)
- Different data types (int, float, string, datetime)
- Both return types for each test

**Performance** (add to `tests/benchmark_tests.ipynb`):
- Multiple dataset sizes (100K, 1M, 10M rows)
- Time comparison: qutePandas vs pandas
- Memory usage comparison (if applicable)
- Speedup calculations

### Running Tests

Before submitting your PR:

```bash
# 1. Run verification tests
python tests/test_pykx_setup.py

# 2. Open and run your test notebooks
jupyter notebook tests/benchmark_tests.ipynb
jupyter notebook tests/edge_cases.ipynb

# 3. Ensure all cells execute without errors
```

---

## Documentation Requirements

All contributions MUST include documentation:

### 1. Docstrings

Every function must have a comprehensive docstring.


### 2. Code Comments

- **DO**: Add comments explaining complex q queries or non-obvious logic
- **DON'T**: Add redundant comments that just restate the code

Good example:
```python
# Convert pandas datetime to q timestamp format (nanoseconds since 2000-01-01)
q_query = f'{{update time:`timestamp$time from x}}'
```

Bad example:
```python
# Call the q function
result = kx.q(query, table)  # This comment is redundant
```

### 3. Documentation Files

If your contribution adds user-facing functionality, update:

- **`docs/usage.html`**: Add examples showing how to use your function
- **`README.md`**: Update if your change affects the quick start or main features
- **Module README** (if applicable): Update module-specific documentation

---

## Benchmarking Requirements

All new functions MUST include performance benchmarks in `tests/benchmark_tests.ipynb`.

### Adding Benchmarks

1. **Open the benchmark notebook**:
   ```bash
   jupyter notebook tests/benchmark_tests.ipynb
   ```

2. **Add a new section** for your function with a markdown cell:
   ```markdown
   ## Benchmark: your_function_name
   
   Description of what this function does and what we're benchmarking.
   ```

3. **Add benchmark code** in a new cell:


### What to Benchmark

- **Multiple dataset sizes**: Test with 100K, 1M, and 10M rows minimum
- **Different data types**: Test with numeric, string, and datetime data where applicable
- **Memory usage**: Compare memory footprint if relevant
- **Correctness**: Always verify results match pandas

### Benchmark Checklist

Before submitting your PR, ensure:

- [ ] Added benchmark to `tests/benchmark_tests.ipynb`
- [ ] Tested with at least 3 different dataset sizes
- [ ] Verified correctness (results match pandas)
- [ ] Benchmark shows performance improvement over pandas (or explains if not)
- [ ] All benchmark cells execute without errors

---

## Code Style

### Python Style

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Keep functions **focused and single-purpose**
- Use **descriptive variable names**

### Project Architecture

qutePandas follows a specific architecture that MUST be followed:

1. **Input Handling**: Accept pandas DataFrames or PyKX Tables
2. **Q-Bound Execution**: ALL computation MUST happen in kdb+/q using q queries (NO pandas/numpy operations)
3. **Dual Return Type Support**: EVERY function MUST support both `return_type='p'` and `return_type='q'`
4. **No Intermediate Pandas**: NEVER use pandas as an intermediate data structure for computation
5. **Performance First**: The whole point is kdb+ speed - don't fall back to pandas operations

Example structure:

```python
def your_function(table, param, return_type='p'):
    """Docstring here"""
    # Convert input to PyKX Table if needed
    if isinstance(table, pd.DataFrame):
        table = kx.toq(table)
    
    # ✅ CORRECT: Execute q query (all computation in kdb+)
    q_query = f'{{your q code here}}'
    result = kx.q(q_query, table)
    
    # ✅ MANDATORY: Support both return types
    if return_type == 'p':
        return result.pd()  # Return pandas DataFrame
    return result  # Return PyKX Table

# ❌ WRONG: Don't do this!
def wrong_function(table, param, return_type='p'):
    # ❌ Converting to pandas for computation defeats the purpose!
    pdf = table.pd()
    result = pdf.some_pandas_operation()  # This is NOT allowed!
    return result
```

### Module Organization

Place your function in the appropriate module:

- **`core/`**: Core DataFrame operations (creation, conversion)
- **`indexing/`**: Indexing and selection operations
- **`transformation/`**: Data transformation (cast, rename, etc.)
- **`cleaning/`**: Data cleaning (drop nulls, fill, etc.)
- **`grouping/`**: Groupby and aggregation operations
- **`joining/`**: Merge and join operations
- **`apply/`**: Apply functions (sum, mean, etc.)
- **`io/`**: Input/output operations
- **`introspection/`**: Introspection functions (dtypes, shape, etc.)

---

## Questions and Support

### Getting Help

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check [docs/](docs/) for detailed guides

### Communication

When asking for help:

1. **Be specific**: Describe what you're trying to do
2. **Provide context**: Include code snippets and error messages
3. **Show effort**: Explain what you've already tried
4. **Be patient**: Maintainers are volunteers

---

## Recognition

Significant contributors will be recognized in:

- **CONTRIBUTORS.md** file (if created in the future)
- **Release notes** for significant contributions
- **Documentation** for major features

---

## License

By contributing to qutePandas, you agree that your contributions will be licensed under the same license as the project (see [LICENSE](LICENSE)).

---

## Thank You! 🎉

Thank you for contributing to qutePandas! Your efforts help make high-performance data processing accessible to the Python community.

For questions about this guide, please open an issue.

---

**Happy Contributing!** 🚀

*Last updated: January 2026*
