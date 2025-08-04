#!/usr/bin/env python3
"""
Test script to check if markdown module is available.
"""

import sys

def test_markdown():
    """Test if markdown module is available."""
    try:
        import markdown
        print("✅ Markdown module is available")
        print(f"   Version: {markdown.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Markdown module not found: {e}")
        return False

def test_other_deps():
    """Test other commonly missing dependencies."""
    deps = [
        "chromadb",
        "crewai", 
        "streamlit",
        "openai",
        "pandas",
        "numpy"
    ]
    
    results = {}
    for dep in deps:
        try:
            __import__(dep)
            results[dep] = True
            print(f"✅ {dep} is available")
        except ImportError as e:
            results[dep] = False
            print(f"❌ {dep} not found: {e}")
    
    return results

if __name__ == "__main__":
    print("🧪 Testing dependencies...")
    print("=" * 40)
    
    markdown_ok = test_markdown()
    other_deps = test_other_deps()
    
    print("\n📊 Summary:")
    print(f"Markdown: {'✅' if markdown_ok else '❌'}")
    
    missing_count = sum(1 for ok in other_deps.values() if not ok)
    if missing_count == 0:
        print("🎉 All dependencies are available!")
        print("You can run: streamlit run streamlit_app.py")
    else:
        print(f"⚠️  {missing_count} dependencies are missing")
        print("Run: python fix_missing_deps.py") 