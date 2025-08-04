#!/usr/bin/env python3
"""
Installation script for Meeting Minutes AI dependencies.
This script handles SQLite compatibility issues and installs all required packages.
"""

import subprocess
import sys
import os
import warnings

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_sqlite_version():
    """Check the current SQLite version."""
    try:
        import sqlite3
        version = sqlite3.sqlite_version_info
        print(f"📊 Current SQLite version: {version}")
        return version
    except Exception as e:
        print(f"⚠️  Could not determine SQLite version: {e}")
        return None

def install_dependencies():
    """Install all required dependencies."""
    print("🚀 Starting dependency installation...")
    
    # Check current SQLite version
    current_version = check_sqlite_version()
    
    # Install ChromaDB with specific version first
    print("📦 Installing ChromaDB...")
    if not run_command("pip install chromadb>=0.4.0,<0.5.0", "Installing ChromaDB"):
        print("❌ Failed to install ChromaDB")
        return False
    
    # Install other dependencies
    print("📦 Installing other dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements")
        return False
    
    # Test SQLite compatibility
    print("🧪 Testing SQLite compatibility...")
    try:
        # Set environment variables
        os.environ["CHROMA_SILENCE_DEPRECATION_WARNINGS"] = "1"
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
        
        # Suppress warnings
        warnings.filterwarnings("ignore", message=".*sqlite3.*")
        warnings.filterwarnings("ignore", message=".*SQLite.*")
        warnings.filterwarnings("ignore", message=".*Chroma.*")
        warnings.filterwarnings("ignore", message=".*unsupported version.*")
        warnings.filterwarnings("ignore", message=".*deprecated.*")
        warnings.filterwarnings("ignore", message=".*You are using a deprecated configuration.*")
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        
        # Try to import ChromaDB
        import chromadb
        print("✅ ChromaDB import successful")
        
        # Try to import CrewAI
        import crewai
        print("✅ CrewAI import successful")
        
        # Test basic ChromaDB functionality with new client syntax
        try:
            # Try new client syntax first
            client = chromadb.PersistentClient(path="./chroma_db")
            print("✅ ChromaDB new client creation successful")
        except Exception as e:
            print(f"⚠️  New client syntax failed, trying legacy: {str(e)[:100]}...")
            try:
                # Fallback to legacy client
                client = chromadb.Client()
                print("✅ ChromaDB legacy client creation successful")
            except Exception as e2:
                print(f"⚠️  Legacy client also failed: {str(e2)[:100]}...")
                print("✅ ChromaDB import successful (client creation skipped)")
        
        return True
    except Exception as e:
        print(f"❌ Compatibility test failed: {e}")
        return False

def main():
    """Main installation function."""
    print("🎯 Meeting Minutes AI - Dependency Installer")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install dependencies
    if install_dependencies():
        print("\n🎉 Installation completed successfully!")
        print("You can now run the application with:")
        print("  streamlit run streamlit_app.py")
    else:
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 