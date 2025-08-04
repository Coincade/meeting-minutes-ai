#!/usr/bin/env python3
"""
Installation script for Meeting Minutes AI
Handles SQLite compatibility issues and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Meeting Minutes AI...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # SQLite compatibility note
    print("📦 Note: Using SQLite compatibility patch instead of pysqlite3...")
    print("   The application includes a patch to work around SQLite version issues.")
    
    # Install the package in development mode
    print("📦 Installing package dependencies...")
    if not run_command("pip install -e .", "Installing package in development mode"):
        print("❌ Failed to install package dependencies")
        sys.exit(1)
    
    # Install additional requirements if requirements.txt exists
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print("📦 Installing additional requirements...")
        if not run_command("pip install -r requirements.txt", "Installing requirements"):
            print("❌ Failed to install requirements")
            sys.exit(1)
    
    print("🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Set up your .env file with your API keys")
    print("2. Run the Streamlit app: streamlit run streamlit_app.py")
    print("3. Or run the main script: python src/meeting_minutes/main.py")
    print("\n💡 If you encounter SQLite errors:")
    print("   - The application includes a compatibility patch")
    print("   - If issues persist, try upgrading your system SQLite to version 3.35.0 or higher")

if __name__ == "__main__":
    main() 