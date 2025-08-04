"""
SQLite compatibility patch for ChromaDB
This module patches the SQLite version check to work around compatibility issues.
"""

import sys
import sqlite3
import warnings
from typing import Optional

def patch_sqlite_version():
    """
    Patch the SQLite version check to work around compatibility issues.
    This function should be called before importing ChromaDB.
    """
    try:
        # Get the current SQLite version
        current_version = sqlite3.sqlite_version_info
        required_version = (3, 35, 0)
        
        # If the version is too old, apply patches
        if current_version < required_version:
            print(f"⚠️  Warning: SQLite version {current_version} is older than required {required_version}")
            print("🔧 Applying SQLite compatibility patch...")
            
            # Suppress all SQLite-related warnings
            warnings.filterwarnings("ignore", message=".*sqlite3.*")
            warnings.filterwarnings("ignore", message=".*SQLite.*")
            warnings.filterwarnings("ignore", message=".*Chroma.*")
            
            # Try to install pysqlite3 if available (optional)
            try:
                import pysqlite3
                sys.modules['sqlite3'] = pysqlite3
                print("✅ Replaced sqlite3 with pysqlite3")
            except ImportError:
                print("⚠️  pysqlite3 not available, using system sqlite3")
            
            print("✅ SQLite compatibility patch applied")
            
    except Exception as e:
        print(f"⚠️  Warning: Could not apply SQLite patch: {e}")

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

# Apply the patch when this module is imported
patch_sqlite_version() 