# SQLite compatibility fix
import sys
import warnings

# Suppress SQLite version warnings
warnings.filterwarnings("ignore", message=".*sqlite3.*")
warnings.filterwarnings("ignore", message=".*SQLite.*")

# Try to import and apply SQLite patch
try:
    from .sqlite_patch import patch_sqlite_version
    patch_sqlite_version()
except ImportError:
    pass
