"""
🔍 Environment Verification Script
Run this FIRST to ensure everything is properly set up

This checks:
1. Python version
2. Required packages
3. GPU availability
4. Data file exists
5. Directory structure
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("\n" + "="*70)
    print("1. CHECKING PYTHON VERSION")
    print("="*70)
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ ERROR: Python 3.8+ required!")
        return False
    
    print("   ✅ Python version OK")
    return True


def check_packages():
    """Check required packages"""
    print("\n" + "="*70)
    print("2. CHECKING REQUIRED PACKAGES")
    print("="*70)
    
    required = {
        'torch': '2.0.0',
        'numpy': '1.21.0',
        'pandas': '1.3.0',
        'scikit-learn': '1.0.0',
        'matplotlib': '3.4.0',
        'seaborn': '0.11.0',
        'tqdm': '4.62.0',
        'scipy': '1.7.0',
    }
    
    import_names = {
    'scikit-learn': 'sklearn',
    }
    
    missing = []
    outdated = []
    
    for package, min_version in required.items():
        try:
            import_name = import_names.get(package, package.replace('-', '_'))
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {package:20s} {version}")
        except ImportError:
            print(f"   ❌ {package:20s} NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n   ❌ Missing packages: {', '.join(missing)}")
        print(f"\n   Install with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("\n   ✅ All packages installed")
    return True


def check_gpu():
    """Check GPU availability"""
    print("\n" + "="*70)
    print("3. CHECKING GPU AVAILABILITY")
    print("="*70)
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"   ✅ GPU: {gpu_name}")
            print(f"   ✅ Memory: {gpu_memory:.1f} GB")
            
            if gpu_memory < 4:
                print(f"   ⚠️  WARNING: Less than 4GB GPU memory!")
                print(f"   ⚠️  Consider using smaller batch sizes")
            
            return True
        else:
            print("   ⚠️  No GPU detected - will use CPU")
            print("   ⚠️  Training will be MUCH slower (~10x)")
            return True
    
    except Exception as e:
        print(f"   ❌ Error checking GPU: {e}")
        return False


def check_data_file():
    """Check if data file exists"""
    print("\n" + "="*70)
    print("4. CHECKING DATA FILE")
    print("="*70)
    
    # Common locations
    possible_paths = [
        Path("/mnt/user-data/uploads/BindingDB.csv"),
        Path("E:/Drug_Protein_Interaction/data/BindingDB.csv"),
        Path("./data/BindingDB.csv"),
        Path("./BindingDB.csv"),
    ]
    
    for path in possible_paths:
        if path.exists():
            size_mb = path.stat().st_size / 1e6
            print(f"   ✅ Found: {path}")
            print(f"   ✅ Size: {size_mb:.1f} MB")
            return True, str(path)
    
    print("   ❌ BindingDB.csv not found in common locations:")
    for path in possible_paths:
        print(f"      - {path}")
    
    print("\n   Please provide the full path to your data file:")
    return False, None


def create_directories():
    """Create necessary directories"""
    print("\n" + "="*70)
    print("5. CREATING DIRECTORY STRUCTURE")
    print("="*70)
    
    dirs = [
        'data_processed',
        'models_saved',
        'results',
        'plots',
        'logs',
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ Created: {dir_name}/")
    
    return True


def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("🔍 ENVIRONMENT VERIFICATION")
    print("="*70)
    
    checks = {
        'Python version': check_python_version(),
        'Required packages': check_packages(),
        'GPU availability': check_gpu(),
        'Data file': check_data_file()[0],
        'Directories': create_directories(),
    }
    
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:20s}: {status}")
    
    if all(checks.values()):
        print("\n✅ ALL CHECKS PASSED - Ready to proceed!")
        print("\nNext step: Run 01_data_explorer.py")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED - Fix issues before proceeding!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
