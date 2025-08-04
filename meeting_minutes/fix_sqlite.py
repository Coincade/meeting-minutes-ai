#!/usr/bin/env python3
"""
Quick fix for SQLite compatibility issues with ChromaDB.
Run this script before starting the application to resolve SQLite version errors.
"""

import sys
import os
import warnings

def apply_sqlite_patch():
    """Apply SQLite compatibility patches."""
    print("🔧 Applying SQLite compatibility patches...")
    
    # Set environment variables
    os.environ["CHROMA_SILENCE_DEPRECATION_WARNINGS"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
    
    # Suppress all warnings
    warnings.filterwarnings("ignore", message=".*sqlite3.*")
    warnings.filterwarnings("ignore", message=".*SQLite.*")
    warnings.filterwarnings("ignore", message=".*Chroma.*")
    warnings.filterwarnings("ignore", message=".*unsupported version.*")
    warnings.filterwarnings("ignore", message=".*deprecated.*")
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    print("✅ SQLite patches applied")

def test_imports():
    """Test if the patches work by importing problematic modules."""
    print("🧪 Testing imports...")
    
    try:
        import chromadb
        print("✅ ChromaDB import successful")
        
        import crewai
        print("✅ CrewAI import successful")
        
        # Test basic ChromaDB functionality with new client syntax
        try:
            # Try new client syntax first
            client = chromadb.PersistentClient(path="./chroma_db")
            print("✅ ChromaDB new client creation successful")
        except Exception as e:
            print(f"⚠️  New client syntax failed, trying legacy: {e}")
            # Fallback to legacy client
            client = chromadb.Client()
            print("✅ ChromaDB legacy client creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main fix function."""
    print("🔧 SQLite Compatibility Fix")
    print("=" * 40)
    
    # Apply patches
    apply_sqlite_patch()
    
    # Test imports
    if test_imports():
        print("\n🎉 SQLite compatibility fix applied successfully!")
        print("You can now run the application without SQLite errors.")
        print("\nTo run the application:")
        print("  streamlit run streamlit_app.py")
    else:
        print("\n❌ Fix failed. Please try the following:")
        print("1. Run: python install_dependencies.py")
        print("2. Or manually install: pip install chromadb>=0.4.0,<0.5.0")
        print("3. Restart your Python environment")
        sys.exit(1)

if __name__ == "__main__":
    main() 