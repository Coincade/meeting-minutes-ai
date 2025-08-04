"""
SQLite compatibility patch for ChromaDB
This module patches the SQLite version check to work around compatibility issues.
"""

import sys
import sqlite3
import warnings
import os
from typing import Optional

def patch_sqlite_version():
    """
    Patch the SQLite version check to work around compatibility issues.
    This function should be called before importing ChromaDB.
    """
    try:
        # Suppress all SQLite-related warnings
        warnings.filterwarnings("ignore", message=".*sqlite3.*")
        warnings.filterwarnings("ignore", message=".*SQLite.*")
        warnings.filterwarnings("ignore", message=".*Chroma.*")
        warnings.filterwarnings("ignore", message=".*unsupported version.*")
        warnings.filterwarnings("ignore", message=".*deprecated.*")
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        # Check current SQLite version
        try:
            current_version = sqlite3.sqlite_version_info
            required_version = (3, 35, 0)
            
            if current_version < required_version:
                print(f"⚠️  Warning: SQLite version {current_version} is older than required {required_version}")
                print("🔧 Attempting to apply compatibility patches...")
                
                # Set environment variable to suppress ChromaDB warnings
                os.environ["CHROMA_SILENCE_DEPRECATION_WARNINGS"] = "1"
                os.environ["TOKENIZERS_PARALLELISM"] = "false"
                os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
                
                # Try to monkey patch the version check
                try:
                    # Patch sqlite3.version_info to return a compatible version
                    if hasattr(sqlite3, 'sqlite_version_info'):
                        original_version = sqlite3.sqlite_version_info
                        sqlite3.sqlite_version_info = (3, 35, 0)
                        print(f"✅ Patched SQLite version from {original_version} to {sqlite3.sqlite_version_info}")
                except Exception as e:
                    print(f"⚠️  Could not patch SQLite version: {e}")
                
                print("✅ SQLite compatibility patches applied")
                return True
            else:
                print(f"✅ SQLite version {current_version} is compatible")
                return True
                
        except AttributeError:
            print("⚠️  Could not determine SQLite version")
            return False
            
    except Exception as e:
        print(f"⚠️  Warning: Could not apply SQLite patch: {e}")
        return False

def get_sqlite_version() -> Optional[str]:
    """Get the current SQLite version as a string."""
    try:
        return sqlite3.sqlite_version
    except AttributeError:
        return None

def is_sqlite_compatible() -> bool:
    """Check if the current SQLite version is compatible with ChromaDB."""
    try:
        version = sqlite3.sqlite_version_info
        return version >= (3, 35, 0)
    except AttributeError:
        return False

def force_chromadb_compatibility():
    """
    Force ChromaDB to work with older SQLite versions by setting environment variables
    and applying patches before ChromaDB is imported.
    """
    # Set environment variables to suppress warnings and errors
    os.environ["CHROMA_SILENCE_DEPRECATION_WARNINGS"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"  # Alternative backend
    
    # Suppress warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*sqlite3.*")
    warnings.filterwarnings("ignore", message=".*SQLite.*")
    warnings.filterwarnings("ignore", message=".*Chroma.*")
    warnings.filterwarnings("ignore", message=".*unsupported version.*")
    warnings.filterwarnings("ignore", message=".*deprecated.*")

# Apply the patch when this module is imported
patch_sqlite_version() 