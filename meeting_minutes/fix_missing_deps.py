#!/usr/bin/env python3
"""
Quick fix for missing dependencies.
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install missing dependencies."""
    print("🔧 Installing missing dependencies...")
    
    # List of commonly missing dependencies
    missing_deps = [
        "markdown>=3.0.0",
        "chromadb>=0.4.0,<0.6.0",
        "crewai[tools]>=0.148.0,<0.153.0"
    ]
    
    success_count = 0
    for dep in missing_deps:
        if install_package(dep):
            success_count += 1
    
    print(f"\n📊 Installed {success_count}/{len(missing_deps)} dependencies")
    
    if success_count == len(missing_deps):
        print("🎉 All dependencies installed successfully!")
        print("You can now run: streamlit run streamlit_app.py")
    else:
        print("⚠️  Some dependencies failed to install. Please check the errors above.")

if __name__ == "__main__":
    main() 