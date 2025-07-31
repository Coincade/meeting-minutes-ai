#!/usr/bin/env python
"""
Setup script for Gmail API configuration
"""
import os
import sys

def setup_environment():
    """Help user set up environment variables"""
    print("Gmail API Setup")
    print("=" * 50)
    
    # Get current values
    current_sender = os.getenv("GMAIL_SENDER", "")
    current_recipient = os.getenv("GMAIL_RECIPIENT", "")
    
    print(f"Current GMAIL_SENDER: {current_sender}")
    print(f"Current GMAIL_RECIPIENT: {current_recipient}")
    
    # Get new values from user
    print("\nPlease enter your email configuration:")
    
    sender = input("Enter your Gmail address (sender): ").strip()
    if not sender:
        sender = current_sender
    
    recipient = input("Enter recipient email address: ").strip()
    if not recipient:
        recipient = current_recipient
    
    # Set environment variables for current session
    os.environ["GMAIL_SENDER"] = sender
    os.environ["GMAIL_RECIPIENT"] = recipient
    
    print(f"\nEnvironment variables set:")
    print(f"GMAIL_SENDER: {sender}")
    print(f"GMAIL_RECIPIENT: {recipient}")
    
    # Create .env file
    env_content = f"""# Gmail API Configuration
GMAIL_SENDER={sender}
GMAIL_RECIPIENT={recipient}
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("\n✓ .env file created successfully!")
    except Exception as e:
        print(f"\n✗ Could not create .env file: {e}")
    
    return sender, recipient

def test_email_send():
    """Test sending an email"""
    print("\n" + "=" * 50)
    print("Testing Email Send")
    print("=" * 50)
    
    try:
        # Add the src directory to the path
        sys.path.append('src/meeting_minutes')
        
        from crews.gmailcrew.tools.gmail_tool import GmailTool
        
        # Create GmailTool instance
        gmail_tool = GmailTool()
        
        # Test email body
        test_body = """
# Test Email from Meeting Minutes Bot

This is a test email to verify that the Gmail API is working correctly.

## Test Details:
- **Sender**: {sender}
- **Recipient**: {recipient}
- **Subject**: Meeting Minutes Test

If you receive this email, the Gmail API integration is working!

Best regards,
Your Meeting Minutes Bot
        """.format(
            sender=os.getenv("GMAIL_SENDER"),
            recipient=os.getenv("GMAIL_RECIPIENT")
        )
        
        print("Sending test email...")
        print(f"From: {os.getenv('GMAIL_SENDER')}")
        print(f"To: {os.getenv('GMAIL_RECIPIENT')}")
        print(f"Subject: Meeting Minutes Test")
        
        # Send the email
        result = gmail_tool._run(test_body)
        print(f"\nResult: {result}")
        
        if "successfully" in result.lower():
            print("\n✓ Email sent successfully!")
            print("Check the recipient's inbox for the test email.")
        else:
            print("\n✗ Email sending failed!")
            print("Check the error message above for details.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPossible issues:")
        print("1. Missing Google API credentials (credentials.json)")
        print("2. Missing required Python packages")
        print("3. OAuth authentication not completed")
        return False

def main():
    # Setup environment
    sender, recipient = setup_environment()
    
    if sender and recipient:
        # Test email sending
        test_email_send()
    else:
        print("\n✗ Please provide both sender and recipient email addresses.")

if __name__ == "__main__":
    main() 