#!/usr/bin/env python
"""
Test script to check GmailCrew instantiation
"""
import os
import sys

# Add the src directory to the path
sys.path.append('src/meeting_minutes')

def test_gmail_crew():
    """Test if GmailCrew can be instantiated"""
    try:
        print("Testing GmailCrew instantiation...")
        
        from crews.gmailcrew.gmailcrew import GmailCrew
        
        # Try to create GmailCrew instance
        crew = GmailCrew()
        print("✓ GmailCrew instantiated successfully!")
        
        # Try to get the crew
        crew_instance = crew.crew()
        print("✓ Crew created successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    test_gmail_crew() 