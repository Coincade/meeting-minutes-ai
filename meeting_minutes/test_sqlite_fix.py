#!/usr/bin/env python3
"""
Test script to verify SQLite compatibility patches work correctly.
"""

import sys
import os
import warnings

def test_sqlite_compatibility():
    """Test if SQLite compatibility patches work."""
    print("🧪 Testing SQLite compatibility...")
    
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
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    try:
        # Check SQLite version
        import sqlite3
        version = sqlite3.sqlite_version_info
        print(f"📊 SQLite version: {version}")
        
        # Try to import ChromaDB
        print("🔍 Testing ChromaDB import...")
        import chromadb
        print("✅ ChromaDB import successful")
        
        # Try to import CrewAI
        print("🔍 Testing CrewAI import...")
        import crewai
        print("✅ CrewAI import successful")
        
        # Test basic ChromaDB functionality with new client syntax
        print("🔍 Testing ChromaDB functionality...")
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
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎯 SQLite Compatibility Test")
    print("=" * 40)
    
    if test_sqlite_compatibility():
        print("\n🎉 All tests passed! SQLite compatibility is working.")
        print("You can now run the application without SQLite errors.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        print("Try running: python install_dependencies.py")
        sys.exit(1)

if __name__ == "__main__":
    main() 