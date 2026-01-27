# Contributing to qutePandas

Thank you for your interest in contributing to **qutePandas**.  
This project provides a **pandas-like API with all computation executed in kdb+/q**.  
Performance, correctness, and clarity are treated as first-class requirements.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Scope](#contribution-scope)
- [Contribution Rules](#contribution-rules)
- [Mandatory Requirements for New Functions](#mandatory-requirements-for-new-functions)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation Requirements](#documentation-requirements)
- [Benchmarking Requirements](#benchmarking-requirements)
- [Code Style and Architecture](#code-style-and-architecture)
- [License](#license)

---

## Code of Conduct

qutePandas is committed to maintaining a respectful, inclusive, and professional environment.  
All contributors are expected to communicate constructively and act in good faith.

---

## Getting Started

Before contributing:

1. Review existing Issues and Pull Requests.
2. Open an issue for major changes or new features.
3. Fork the repository and create a feature branch.

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- PyKX (licensed or unlicensed mode)
- Git

### Setup Instructions

```bash
git clone https://github.com/YOUR_USERNAME/qutePandas.git
cd qutePandas

python3 -m venv venv_dev
source venv_dev/bin/activate   # macOS/Linux
# venv_dev\Scripts\activate    # Windows

pip install -e .
pip install -r requirements-dev.txt
```

### PyKX Configuration

**Unlicensed mode (recommended for development):**
```bash
export PYKX_UNLICENSED=true
```

**Licensed mode:**
Place `kc.lic` in a valid license directory or project root.

### Verify Setup
```bash
python tests/test_pykx_setup.py
```

---

## Contribution Scope

Contributions are welcome in the following areas:
- Pandas-like APIs implemented using kdb+/q
- Performance optimizations in q
- Bug fixes
- Documentation improvements
- Test and benchmark coverage

---

## Contribution Rules

### Required
- All computation **MUST** be executed in kdb+/q.
- Every function **MUST** support `return_type='p'` (pandas) and `return_type='q'` (PyKX).
- Functions must accept both pandas DataFrames and PyKX Tables as input.
- Comprehensive docstrings are mandatory.
- Tests and benchmarks are mandatory.

### Forbidden
- Pandas or NumPy used for computation.
- Pandas used as an intermediate data structure.
- APIs that do not align with pandas semantics.
- Untested or unbenchmarked features.

---

## Mandatory Requirements for New Functions

Every new function **MUST** update documentation and include tests/benchmarks. Pull requests that do not meet these requirements will not be reviewed.

### 1. Documentation Updates
- **docs/usage.html**: Add a clear usage example with both return types.
- **docs/benchmarks.html**: Reference the new benchmark results and explain performance benefits.

### 2. Testing Updates
- **tests/edge_cases.ipynb**: Cover empty DataFrames, single row/col, null values, and type variations. Results must match pandas behavior.

### 3. Performance Benchmarks
- **tests/benchmark_tests.ipynb**: Test at 100K, 1M, and 10M rows. Compare against pandas.

---

## Pull Request Process

### Pull Request Checklist
- [ ] Implementation uses kdb+/q only
- [ ] Supports `return_type='p'` and `return_type='q'`
- [ ] Added usage documentation (`docs/usage.html`)
- [ ] Added benchmark documentation (`docs/benchmarks.html`)
- [ ] Added edge case tests (`tests/edge_cases.ipynb`)
- [ ] Added performance benchmarks (`tests/benchmark_tests.ipynb`)
- [ ] Verified correctness against pandas
- [ ] All tests and notebooks run without errors

---

## Testing Requirements

All tests must be added to existing notebooks:
- **Correctness**: `tests/edge_cases.ipynb`
- **Performance**: `tests/benchmark_tests.ipynb`

### Running Tests
```bash
python tests/test_pykx_setup.py
# Then manually run:
# jupyter notebook tests/edge_cases.ipynb
# jupyter notebook tests/benchmark_tests.ipynb
```

---

## Code Style and Architecture

### Mandatory Execution Flow
```python
def function(table, return_type='p'):
    # Input conversion
    if isinstance(table, pd.DataFrame):
        table = kx.toq(table)

    # All computation in q
    result = kx.q("{ q logic here }", table)

    # Dual return type support
    if return_type == 'p':
        return result.pd()
    return result
```

---

## License

By contributing to qutePandas, you agree that your contributions are licensed under the same terms as the project (MIT License).

---

**Thank You!**  
Your contributions help advance high-performance data processing in Python. Quality, correctness, and performance matter here.

*Last updated: January 2026*
