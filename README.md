# qutePandas

A pandas-like library for kdb+/q powered by [PyKX](https://github.com/KxSystems/pykx).

While Pandas is the gold standard for data manipulation in Python, it often struggles with memory overhead and execution speed when handling multi-gigabyte datasets or complex time-series operations. `qutePandas` addresses these limitations by offloading compute-intensive operations to the kdb+/q engine, leveraging its columnar architecture and high-performance vector processing. By providing a familiar pandas-like API, it allows Python engineers to achieve kdb+ speeds without leaving the Python ecosystem.

## Installation

```bash
pip install qutePandas
```

*Note: Requires a kdb+ license and the PyKX library.*

## Quick Start

```python
import qutePandas as qpd
import pandas as pd

# Convert a pandas DataFrame to a qutePandas table
df = pd.DataFrame({
    "time": pd.date_range("2023-01-01", periods=1000000, freq="ms"),
    "price": pd.Series(range(1000000))
})
q_table = qpd.DataFrame(df)

# Perform high-performance aggregation
# Computation happens in kdb+
res = qpd.apply(q_table, "sum", axis=0, return_type="p")
print(res)
```

## Documentation

Full documentation, including API reference and performance benchmarks, is available at:
[https://ishapatro.github.io/qutePandas/](https://ishapatro.github.io/qutePandas/)

## GitHub

The source code for this project is available on GitHub at:
[https://github.com/ishapatro/qutePandas](https://github.com/ishapatro/qutePandas)

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](https://github.com/IshaPatro/qutePandas/blob/main/CONTRIBUTING.md) for more information.

## License

MIT License

## Author

Created by [Isha Patro](https://ishapatro.in)