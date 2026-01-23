# PyKX and kdb+ Installation Guide

This guide provides detailed steps for installing PyKX, setting up kdb+ licenses, and configuring your environment for qutePandas.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [kdb+ Installation](#kdb-installation)
3. [PyKX Installation](#pykx-installation)
4. [License Setup](#license-setup)
5. [Environment Configuration](#environment-configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.7+ (recommended: 3.8 or higher)
- **Memory**: At least 4GB RAM (8GB+ recommended for large datasets)
- **Architecture**: x86_64 (ARM/M1 Macs supported with specific builds)

### Required Tools

```bash
# Ensure you have these tools installed
python --version  # Should be 3.7+
pip --version     # Latest version recommended
```

## kdb+ Installation

### Option 1: Free Personal Edition

1. **Download kdb+ Personal Edition**:
   - Visit [Kx Systems Download](https://kx.com/connect-with-us/download/)
   - Select "Personal Edition" (free for non-commercial use)
   - Choose your operating system

2. **Install kdb+**:
   ```bash
   # Linux/macOS
   mkdir -p ~/kdb+
   cd ~/kdb+
   # Extract your downloaded kdb+ package here
   
   # Windows
   # Extract to C:\kdb+ or your preferred location
   ```

3. **Set up PATH**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH=$PATH:~/kdb+
   export QHOME=~/kdb+
   ```

### Option 2: Licensed Version

If you have a commercial kdb+ license:

1. Install kdb+ following your license agreement
2. Ensure the license file (`kc.lic` or `k4.lic`) is in the correct location
3. Set environment variables as required by your license

## PyKX Installation

### Step 1: Create Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv_qutepandas
source venv_qutepandas/bin/activate  # Linux/macOS
# OR
venv_qutepandas\Scripts\activate     # Windows
```

### Step 2: Install PyKX

```bash
# Install PyKX (this may take a few minutes)
pip install pykx

# For development/beta features (optional)
pip install pykx[beta]

# Verify installation
python -c "import pykx as kx; print('PyKX version:', kx.__version__)"
```

### Step 3: Install Additional Dependencies

```bash
# Install required dependencies for qutePandas
pip install pandas>=1.3.0
pip install numpy>=1.20.0
```

## License Setup

### For Personal/Free Use

If using kdb+ Personal Edition, PyKX will attempt to use the free license automatically.

### For Commercial/Licensed Use

#### Method 1: Base64 License (Recommended)

If you have a base64-encoded license:

1. **Create license setup script**:
   ```python
   # save as setup_license.py
   import base64
   import os
   
   def setup_license(license_base64):
       # Decode license
       license_data = base64.b64decode(license_base64)
       
       # Create kdb+ directory
       kdb_dir = os.path.expanduser("~/kdb+")
       os.makedirs(kdb_dir, exist_ok=True)
       
       # Save license file
       license_path = os.path.join(kdb_dir, "kc.lic")
       with open(license_path, "wb") as f:
           f.write(license_data)
       
       print(f"License saved to: {license_path}")
       return license_path
   
   # Replace with your actual base64 license
   your_license = "YOUR_BASE64_LICENSE_HERE"
   setup_license(your_license)
   ```

2. **Run the setup script**:
   ```bash
   python setup_license.py
   ```

#### Method 2: Manual License File

1. **Copy your license file**:
   ```bash
   # Copy your kc.lic file to the kdb+ directory
   cp /path/to/your/kc.lic ~/kdb+/
   
   # Verify permissions
   chmod 644 ~/kdb+/kc.lic
   ```

## Environment Configuration

### Set Environment Variables

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, or equivalent):

```bash
# kdb+ Configuration
export QHOME=~/kdb+                    # kdb+ installation directory
export QLIC=~/kdb+                     # License directory
export PATH=$PATH:$QHOME               # Add q to PATH

# PyKX Configuration (optional)
export PYKX_Q_LIB_LOCATION=$QHOME      # PyKX q library location
```

### Reload Environment

```bash
# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc

# Or restart your terminal
```

### Windows Environment Variables

For Windows users, set environment variables through:

1. **System Properties** → **Environment Variables**
2. Add:
   - `QHOME`: `C:\kdb+` (or your installation path)
   - `QLIC`: `C:\kdb+` (or your license path)
   - `PATH`: Add `C:\kdb+` to existing PATH

## Verification

### Test PyKX Installation

```python
# test_pykx.py
import pykx as kx
import pandas as pd

# Test basic functionality
try:
    # Create a simple table
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': ['x', 'y', 'z']
    })
    
    # Convert to q table and back
    q_table = kx.toq(df)
    result_df = q_table.pd()
    
    print("✅ PyKX installation successful!")
    print(f"Original DataFrame:\n{df}")
    print(f"Converted back from q:\n{result_df}")
    
except Exception as e:
    print(f"❌ PyKX installation failed: {e}")
```

### Test qutePandas Integration

```bash
# Navigate to qutePandas directory
cd /path/to/qutePandas

# Install qutePandas
pip install -e .

# Run a simple test
python -c "
import qutePandas as qpd
import pandas as pd

# Test connection
try:
    qpd.connect()
    print('✅ qutePandas connection successful!')
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

## Troubleshooting

### Critical Issue: `licence error: embedq`

> [!IMPORTANT]
> **This is the most common PyKX error with qutePandas**

**Symptoms**:
```
PyKXException: Non-zero qinit following license install with configuration:
{
  'qhome': '/path/to/pykx/lib',
  'qlic': PosixPath('/path/to/kc.lic')
}

failed with output:
'2026.01.22T10:33:12.922 licence error: embedq'
```

**Root Cause**:
PyKX initializes an embedded q process when imported. This error occurs when:
1. The license file doesn't support embedded q mode
2. Environment variables aren't set before PyKX imports
3. No valid license is found and unlicensed mode isn't enabled

**Solution 1: Enable Unlicensed Mode (Recommended for Development)**

qutePandas 1.0.0+ automatically enables unlicensed mode if no license is found. If you're using an older version or need to force it:

```bash
# Set environment variable
export PYKX_UNLICENSED=true

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'export PYKX_UNLICENSED=true' >> ~/.zshrc
source ~/.zshrc

# Restart Python and try again
python -c "import qutePandas as qpd; print('Success!')"
```

**Solution 2: Use a Valid Embedded Q License**

If you have a commercial kdb+ license that supports embedded q:

```bash
# Place license in the correct location
mkdir -p ~/.qutepandas
cp /path/to/your/kc.lic ~/.qutepandas/

# Verify it's there
ls -la ~/.qutepandas/kc.lic

# Restart Python
python -c "import qutePandas as qpd; print('Success!')"
```

**Solution 3: Use License Token**

If you have a base64-encoded license token:

```bash
# Set environment variable
export KX_TOKEN="your-base64-token-here"

# Or add to .env file in project root
echo 'KX_TOKEN="your-base64-token-here"' >> .env
```

**Verification**:

Run the standalone test file to verify your setup:

```bash
cd /path/to/qutePandas
python tests/test_pykx_setup.py
```

This will check your license configuration and verify PyKX + qutePandas are working correctly.

---

### Common Issues and Solutions

#### 1. "No valid q license found"

**Symptoms**:
```
LicenseException: A valid q license must be in a known location
```

**Solutions**:
- Verify `QLIC` environment variable is set: `echo $QLIC`
- Check license file exists: `ls -la $QLIC/kc.lic`
- Ensure license file has correct permissions: `chmod 644 $QLIC/kc.lic`
- Try setting license path explicitly in Python:
  ```python
  import os
  os.environ['QLIC'] = '/path/to/your/license/directory'
  ```

#### 2. "Module not found: pykx"

**Solutions**:
- Verify virtual environment is activated
- Reinstall PyKX: `pip uninstall pykx && pip install pykx`
- Check Python path: `python -c "import sys; print(sys.path)"`

#### 3. "Failed to connect to kdb+"

**Solutions**:
- Check if kdb+ process is running: `ps aux | grep q`
- Verify QHOME is set: `echo $QHOME`
- Test q installation: `q` (should start q REPL)
- Check firewall settings if using remote kdb+ instance

#### 4. Performance Issues

**Solutions**:
- Increase memory: Set `export QMEMSIZE=8000` (8GB)
- Use 64-bit Python and kdb+
- Monitor system resources during large operations

#### 5. M1 Mac Compatibility

**Solutions**:
- Use x86_64 version of Python via Rosetta:
  ```bash
  arch -x86_64 python -m pip install pykx
  ```
- Or use native ARM builds if available
- Check architecture: `python -c "import platform; print(platform.machine())"`

### Getting Additional Help

1. **PyKX Documentation**: [PyKX Docs](https://code.kx.com/pykx/)
2. **kdb+ Documentation**: [kdb+ Docs](https://code.kx.com/q/)
3. **Community Forums**: [Kx Community](https://community.kx.com/)
4. **GitHub Issues**: [PyKX Issues](https://github.com/KxSystems/pykx/issues)

### Debug Information

If you need to report issues, collect this information:

```python
# debug_info.py
import sys
import os
import platform

print("=== System Information ===")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Architecture: {platform.machine()}")
print(f"Python: {sys.version}")

print("\n=== Environment Variables ===")
for var in ['QHOME', 'QLIC', 'PATH', 'PYKX_Q_LIB_LOCATION']:
    print(f"{var}: {os.environ.get(var, 'Not set')}")

print("\n=== PyKX Information ===")
try:
    import pykx as kx
    print(f"PyKX version: {kx.__version__}")
    print("PyKX import: ✅ Success")
except Exception as e:
    print(f"PyKX import: ❌ Failed - {e}")

print("\n=== qutePandas Information ===")
try:
    import qutePandas as qpd
    print(f"qutePandas version: {qpd.__version__}")
    print("qutePandas import: ✅ Success")
except Exception as e:
    print(f"qutePandas import: ❌ Failed - {e}")
```

Run this script and include the output when reporting issues.

---

## Next Steps

After successful installation:

1. **Return to main README**: [README.md](README.md)
2. **Run the test suite**: `python tests/run_all_tests.py`
3. **Try the examples**: Follow the usage examples in the main README
4. **Start developing**: Check the development section for contribution guidelines 