#!/usr/bin/env python
"""
Simple test script to check Gmail API setup
"""
import os
import sys

# Add the src directory to the path
sys.path.append('src/meeting_minutes')

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from crews.gmailcrew.tools.gmail_tool import GmailTool
        print("✓ GmailTool imported successfully")
        
        from crews.gmailcrew.tools.gmail_utility import authenticate_gmail, create_message, send_message
        print("✓ Gmail utility functions imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_credentials():
    """Test if credentials file exists"""
    credentials_path = "src/meeting_minutes/crews/gmailcrew/tools/credentials.json"
    token_path = "src/meeting_minutes/crews/gmailcrew/tools/token.json"
    
    print(f"\nChecking credentials...")
    print(f"Credentials file exists: {os.path.exists(credentials_path)}")
    print(f"Token file exists: {os.path.exists(token_path)}")
    
    if not os.path.exists(credentials_path):
        print("✗ Missing credentials.json file!")
        print("You need to:")
        print("1. Go to Google Cloud Console")
        print("2. Create a project and enable Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download credentials.json and place it in the tools directory")
        return False
    
    return True

def test_environment_variables():
    """Test if required environment variables are set"""
    print(f"\nChecking environment variables...")
    
    sender = os.getenv("GMAIL_SENDER")
    recipient = os.getenv("GMAIL_RECIPIENT")
    
    print(f"GMAIL_SENDER: {sender}")
    print(f"GMAIL_RECIPIENT: {recipient}")
    
    if not sender or not recipient:
        print("✗ Missing environment variables!")
        print("You need to set:")
        print("- GMAIL_SENDER (your Gmail address)")
        print("- GMAIL_RECIPIENT (recipient's email address)")
        return False
    
    return True

def main():
    print("Gmail API Setup Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test credentials
    credentials_ok = test_credentials()
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    print("\n" + "=" * 50)
    if imports_ok and credentials_ok and env_ok:
        print("✓ All tests passed! Gmail API should work.")
    else:
        print("✗ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main() 