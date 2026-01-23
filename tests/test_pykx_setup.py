#!/usr/bin/env python3
"""
PyKX + qutePandas Setup Verification Test

This standalone test file verifies that:
1. PyKX license is properly configured
2. Embedded q initializes successfully
3. qutePandas imports without errors
4. Basic DataFrame operations work correctly

Run this file to diagnose and verify your PyKX + qutePandas setup.
"""

import sys
import os
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def print_result(test_name, passed, message=""):
    """Print a test result with status indicator."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {test_name}")
    if message:
        print(f"       {message}")


def check_python_version():
    """Verify Python version is 3.8 or higher."""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_result("Python Version", True, "Python 3.8+ detected")
        return True
    else:
        print_result("Python Version", False, "Python 3.8+ required")
        return False


def check_license_files():
    """Check for kdb+ license files in common locations."""
    print_section("License File Detection")
    
    locations = [
        Path.home() / ".qutepandas" / "kc.lic",
        Path(__file__).parent.parent / "kdb_lic" / "kc.lic",
        Path.home() / "kdb+" / "kc.lic",
        Path.home() / "q" / "kc.lic",
    ]
    
    found_licenses = []
    for loc in locations:
        if loc.exists():
            found_licenses.append(str(loc))
            print(f"  Found: {loc}")
    
    qlic = os.environ.get('QLIC')
    kx_token = os.environ.get('KX_TOKEN') or os.environ.get('KDB_TOKEN')
    pykx_unlicensed = os.environ.get('PYKX_UNLICENSED')
    
    print(f"\nEnvironment Variables:")
    print(f"  QLIC: {qlic if qlic else 'Not set'}")
    print(f"  KX_TOKEN: {'Set' if kx_token else 'Not set'}")
    print(f"  PYKX_UNLICENSED: {pykx_unlicensed if pykx_unlicensed else 'Not set'}")
    
    if found_licenses or kx_token or pykx_unlicensed == 'true':
        print_result("License Detection", True, 
                    f"Found {len(found_licenses)} license file(s) or valid configuration")
        return True
    else:
        print_result("License Detection", False, 
                    "No license found - will attempt unlicensed mode")
        return False


def test_pykx_import():
    """Test PyKX import and initialization."""
    print_section("PyKX Import and Initialization")
    
    try:
        import pykx as kx
        print(f"PyKX version: {kx.__version__}")
        print_result("PyKX Import", True)
        return True, kx
    except Exception as e:
        print_result("PyKX Import", False, str(e))
        return False, None


def test_embedded_q(kx):
    """Test embedded q functionality."""
    print_section("Embedded Q Initialization")
    
    if kx is None:
        print_result("Embedded Q", False, "PyKX not available")
        return False
    
    try:
        # Test basic q expression
        result = kx.q('1+1')
        expected = 2
        
        if result.py() == expected:
            print_result("Basic Q Expression", True, f"1+1 = {result.py()}")
        else:
            print_result("Basic Q Expression", False, 
                        f"Expected {expected}, got {result.py()}")
            return False
        
        # Test table creation
        table = kx.q('([] a:1 2 3; b:`x`y`z)')
        print(f"Created q table:\n{table}")
        print_result("Q Table Creation", True)
        
        return True
    except Exception as e:
        print_result("Embedded Q", False, str(e))
        return False


def test_qutepandas_import():
    """Test qutePandas import."""
    print_section("qutePandas Import")
    
    try:
        import qutePandas as qpd
        print(f"qutePandas version: {qpd.__version__}")
        print_result("qutePandas Import", True)
        return True, qpd
    except Exception as e:
        print_result("qutePandas Import", False, str(e))
        print(f"\nFull error:\n{e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_qutepandas_operations(qpd):
    """Test basic qutePandas DataFrame operations."""
    print_section("qutePandas DataFrame Operations")
    
    if qpd is None:
        print_result("DataFrame Operations", False, "qutePandas not available")
        return False
    
    try:
        # Test 1: Create DataFrame from dict
        df = qpd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'score': [95.5, 87.3, 92.1, 78.9, 88.4]
        })
        print(f"Created DataFrame:\n{df}")
        print_result("DataFrame Creation", True)
        
        # Test 2: Get dtypes
        dtypes = qpd.dtypes(df)
        print(f"\nDataFrame dtypes:\n{dtypes}")
        print_result("Get Dtypes", True)
        
        # Test 3: Convert to pandas
        pdf = df.pd()
        print(f"\nConverted to pandas:\n{pdf}")
        print_result("Convert to Pandas", True, f"Shape: {pdf.shape}")
        
        # Test 4: Filter operation
        filtered = qpd.apply(df, lambda x: x['score'] > 85)
        print(f"\nFiltered (score > 85):\n{filtered}")
        print_result("Filter Operation", True)
        
        # Test 5: Groupby operation
        df2 = qpd.DataFrame({
            'category': ['A', 'B', 'A', 'B', 'A'],
            'value': [10, 20, 30, 40, 50]
        })
        grouped = qpd.groupby_sum(df2, 'category', 'value')
        print(f"\nGroupby sum:\n{grouped}")
        print_result("Groupby Operation", True)
        
        return True
    except Exception as e:
        print_result("DataFrame Operations", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def print_diagnostic_info():
    """Print diagnostic information for troubleshooting."""
    print_section("Diagnostic Information")
    
    import platform
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version}")
    
    print(f"\nEnvironment Variables:")
    for var in ['QHOME', 'QLIC', 'PYKX_UNLICENSED', 'PYKX_RELEASE_GIL', 
                'PYKX_ENFORCE_EMBEDDED_IMPORT', 'KX_TOKEN', 'KDB_TOKEN']:
        value = os.environ.get(var, 'Not set')
        print(f"  {var}: {value}")
    
    print(f"\nPython Path:")
    for path in sys.path[:5]:
        print(f"  {path}")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  PyKX + qutePandas Setup Verification")
    print("=" * 70)
    
    results = []
    
    # Test 1: Python version
    results.append(check_python_version())
    
    # Test 2: License detection
    results.append(check_license_files())
    
    # Test 3: PyKX import
    pykx_ok, kx = test_pykx_import()
    results.append(pykx_ok)
    
    # Test 4: Embedded q
    if pykx_ok:
        results.append(test_embedded_q(kx))
    else:
        results.append(False)
    
    # Test 5: qutePandas import
    qpd_ok, qpd = test_qutepandas_import()
    results.append(qpd_ok)
    
    # Test 6: qutePandas operations
    if qpd_ok:
        results.append(test_qutepandas_operations(qpd))
    else:
        results.append(False)
    
    # Print diagnostic info
    print_diagnostic_info()
    
    # Summary
    print_section("Test Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 SUCCESS! PyKX + qutePandas is properly configured.")
        return 0
    else:
        print("\n⚠️  ISSUES DETECTED. See failures above for details.")
        print("\nCommon solutions:")
        print("  1. Ensure kc.lic is in ~/.qutepandas/ or project kdb_lic/")
        print("  2. Set PYKX_UNLICENSED=true for unlicensed mode")
        print("  3. Check that Python is 3.8+")
        print("  4. Reinstall: pip install --upgrade pykx")
        return 1


if __name__ == "__main__":
    sys.exit(main())
