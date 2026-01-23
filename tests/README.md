# qutePandas Testing Guide

This guide provides instructions for setting up and running qutePandas tests.

## 📋 Quick Start

### Step 1: Verify Python Version

```bash
python3 --version
# Should show Python 3.8 or higher
```

**Required**: Python 3.8+

If you need to install Python 3.8+:
- **macOS**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt install python3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

---

### Step 2: Create Virtual Environment

```bash
# Navigate to the qutePandas project directory
cd /path/to/qutePandas

# Create virtual environment
python3 -m venv venv_qutepandas

# Activate virtual environment
source venv_qutepandas/bin/activate  # macOS/Linux
# OR
venv_qutepandas\Scripts\activate     # Windows
```

---

### Step 3: Install qutePandas

```bash
# Install in development mode
pip install -e .
```

This will automatically install all dependencies including PyKX.

---

### Step 4: Configure PyKX License

Choose **ONE** of the following options:

#### Option A: Use Unlicensed Mode (Free, Recommended for Testing)

**Important**: If you have a `.env` file in the project root with `QLIC` or `QHOME` set, you need to either:

1. **Remove or comment out** those lines in `.env`:
   ```bash
   # Edit .env file and comment out or remove:
   # QLIC="/some/path"
   # QHOME="/some/path"
   ```

2. **OR ensure the path has a valid license**:
   ```bash
   # Make sure the directory specified in QLIC has kc.lic
   ls -la $(grep QLIC .env | cut -d'=' -f2 | tr -d '"')/kc.lic
   ```

3. **OR override with environment variable**:
   ```bash
   export PYKX_UNLICENSED=true
   ```

If no `.env` file exists or QLIC is not set, unlicensed mode will be enabled automatically.

#### Option B: Use Commercial License

If you have a `kc.lic` file, place it in **one or more** of these locations (in priority order):

1. **Project directory** (recommended for development):
   ```bash
   # Create license directory in project root
   mkdir -p kdb_lic
   
   # Copy your license file
   cp /path/to/your/kc.lic kdb_lic/
   
   # Verify it's there
   ls -la kdb_lic/kc.lic
   ```

2. **User home directory** (recommended for personal use):
   ```bash
   # Create license directory
   mkdir -p ~/.qutepandas
   
   # Copy your license file
   cp /path/to/your/kc.lic ~/.qutepandas/
   
   # Verify it's there
   ls -la ~/.qutepandas/kc.lic
   ```

3. **Tests directory** (optional, for convenience when running tests):
   ```bash
   # Copy license to tests folder
   cp /path/to/your/kc.lic tests/
   
   # Verify it's there
   ls -la tests/kc.lic
   ```

**Tip**: It's recommended to place the license in **both** `kdb_lic/` and `tests/` for maximum convenience. This ensures tests work regardless of where they're run from.


#### Option C: Use License Token

If you have a base64-encoded license token:

```bash
# Set environment variable
export KX_TOKEN="your-base64-token-here"

# Or add to your shell profile for persistence
echo 'export KX_TOKEN="your-base64-token-here"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🧪 Running Tests

### Verification Test

Run the comprehensive setup verification test:

```bash
# From the project root directory
python tests/test_pykx_setup.py
```

**Expected Output** (all tests passing):
```
======================================================================
  PyKX + qutePandas Setup Verification
======================================================================

✅ PASS: Python Version
✅ PASS: License Detection
✅ PASS: PyKX Import
✅ PASS: Basic Q Expression
✅ PASS: Q Table Creation
✅ PASS: qutePandas Import
✅ PASS: DataFrame Creation
✅ PASS: Get Dtypes
✅ PASS: Convert to Pandas
✅ PASS: Filter Operation
✅ PASS: Groupby Operation

Tests Passed: 11/11

🎉 SUCCESS! PyKX + qutePandas is properly configured.
```

### Running Jupyter Notebook Tests

```bash
# Install Jupyter if not already installed
pip install jupyter

# Start Jupyter
jupyter notebook

# Navigate to the tests/ folder and open any .ipynb file
```

---

## 🔧 Troubleshooting

### Error: `licence error: embedq`

**Cause**: PyKX tried to initialize before environment variables were set, or the license doesn't support embedded q mode.

**Solution**:
```bash
# Enable unlicensed mode
export PYKX_UNLICENSED=true

# Restart Python and try again
python tests/test_pykx_setup.py
```

For persistent configuration, add to your shell profile:
```bash
echo 'export PYKX_UNLICENSED=true' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc
```

---

### Error: `No valid q license found`

**Solution**:
```bash
# Enable unlicensed mode
export PYKX_UNLICENSED=true

# Then run tests
python tests/test_pykx_setup.py
```

---

### Error: `Module not found: pykx`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv_qutepandas/bin/activate

# Reinstall PyKX
pip install --upgrade pykx

# Verify installation
python -c "import pykx; print(pykx.__version__)"
```

---

### Error: `ImportError: cannot import name 'DataFrame'`

**Solution**:
```bash
# Reinstall qutePandas in development mode
pip install -e . --force-reinstall --no-deps

# Verify installation
python -c "import qutePandas as qpd; print(qpd.__version__)"
```

---

### Jupyter Notebook Issues

If using Jupyter notebooks, restart the kernel after installing/updating:

1. In the notebook menu: **Kernel** → **Restart Kernel**
2. Or run in a cell:
   ```python
   import sys
   !{sys.executable} -m pip install -e /path/to/qutePandas
   ```
   Then restart the kernel.

---

## 📝 Quick Test in Python REPL

Verify your installation works:

```python
# Test 1: Import qutePandas
import qutePandas as qpd
print(f"qutePandas version: {qpd.__version__}")

# Test 2: Create a DataFrame
df = qpd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'score': [95, 87, 92]
})
print(df)

# Test 3: Convert to pandas
pdf = df.pd()
print(pdf)

# Success! 🎉
```

---

## 🔍 Diagnostic Commands

If you encounter issues, run these commands and share the output:

```bash
# Check Python version
python3 --version

# Check PyKX installation
python -c "import pykx as kx; print('PyKX:', kx.__version__)"

# Check environment variables
echo "QLIC: $QLIC"
echo "PYKX_UNLICENSED: $PYKX_UNLICENSED"
echo "PYKX_RELEASE_GIL: $PYKX_RELEASE_GIL"

# Run full diagnostic test
python tests/test_pykx_setup.py
```

---

## 📚 Additional Resources

- **PyKX Documentation**: https://code.kx.com/pykx/
- **qutePandas Documentation**: See `../docs/` folder
- **kdb+ License**: https://kx.com/connect-with-us/download/
- **Installation Guide**: See `../PYKX_INSTALLATION.md`

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] qutePandas installed (`pip install -e .`)
- [ ] License configured (unlicensed mode or `kc.lic` file)
- [ ] Environment variables set (if needed)
- [ ] Test file passes all checks (`python tests/test_pykx_setup.py`)
- [ ] Can import and use qutePandas in Python

---

## 🚀 Next Steps

After successful setup:

1. **Explore Examples**: Check the test notebooks in this directory
2. **Read Documentation**: Review `../docs/usage.html` for API reference
3. **Run Benchmarks**: See `../docs/benchmarks.html` for performance comparisons
4. **Start Building**: Create your first qutePandas project!
