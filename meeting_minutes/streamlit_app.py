import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

# Add the src directory to the path
sys.path.append('src/meeting_minutes')

# Import your existing modules
from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from crews.gmailcrew.gmailcrew import GmailCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Meeting Minutes Generator",
    page_icon="📝",
    layout="wide"
)

# Title and description
st.title("🎙️ Meeting Minutes Generator")
st.markdown("Upload an audio file to automatically generate meeting minutes and create an email draft.")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Email settings
    st.subheader("Email Settings")
    sender = st.text_input(
        "Sender Email", 
        value=os.getenv("GMAIL_SENDER", ""),
        help="Your Gmail address"
    )
    recipient = st.text_input(
        "Recipient Email", 
        value=os.getenv("GMAIL_RECIPIENT", ""),
        help="Email address to send meeting minutes to"
    )
    
    # Save email settings
    if st.button("💾 Save Email Settings"):
        # Update environment variables for this session
        os.environ["GMAIL_SENDER"] = sender
        os.environ["GMAIL_RECIPIENT"] = recipient
        st.success("Email settings saved!")
    
    st.divider()
    
    # Status
    st.subheader("📊 Status")
    if os.getenv("GMAIL_SENDER") and os.getenv("GMAIL_RECIPIENT"):
        st.success("✅ Email configured")
    else:
        st.error("❌ Email not configured")
    
    if os.path.exists("src/meeting_minutes/crews/gmailcrew/tools/credentials.json"):
        st.success("✅ Gmail credentials found")
    else:
        st.error("❌ Gmail credentials missing")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 Upload Audio File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'm4a', 'flac'],
        help="Supported formats: WAV, MP3, M4A, FLAC"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024 / 1024:.2f} MB",
            "File type": uploaded_file.type
        }
        st.json(file_details)
        
        # Process button
        if st.button("🚀 Generate Meeting Minutes", type="primary"):
            if not sender or not recipient:
                st.error("Please configure email settings in the sidebar first!")
            else:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Save uploaded file
                    status_text.text("📁 Saving audio file...")
                    progress_bar.progress(10)
                    
                    # Create temp directory and save file
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                        with open(temp_audio_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Step 2: Transcribe audio
                        status_text.text("🎙️ Transcribing audio...")
                        progress_bar.progress(30)
                        
                        # Import transcription function
                        from openai import OpenAI
                        from pydub import AudioSegment
                        from pydub.utils import make_chunks
                        
                        client = OpenAI()
                        
                        # Load and chunk audio
                        audio = AudioSegment.from_file(temp_audio_path)
                        chunk_length_ms = 60000  # 1 minute chunks
                        chunks = make_chunks(audio, chunk_length_ms)
                        
                        # Transcribe chunks
                        full_transcription = ""
                        for i, chunk in enumerate(chunks):
                            chunk_path = os.path.join(temp_dir, f"chunk_{i}.wav")
                            chunk.export(chunk_path, format="wav")
                            
                            with open(chunk_path, "rb") as audio_file:
                                transcription = client.audio.transcriptions.create(
                                    model="whisper-1", 
                                    file=audio_file
                                )
                                full_transcription += transcription.text + " "
                        
                        progress_bar.progress(60)
                        
                        # Step 3: Generate meeting minutes
                        status_text.text("📝 Generating meeting minutes...")
                        progress_bar.progress(70)
                        
                        crew = MeetingMinutesCrew()
                        inputs = {"transcript": full_transcription}
                        meeting_minutes = crew.crew().kickoff(inputs)
                        
                        # Convert to string
                        if hasattr(meeting_minutes, 'raw'):
                            meeting_minutes_str = str(meeting_minutes.raw)
                        else:
                            meeting_minutes_str = str(meeting_minutes)
                        
                        progress_bar.progress(85)
                        
                        # Step 4: Create email draft
                        status_text.text("📧 Creating email draft...")
                        progress_bar.progress(90)
                        
                        gmail_crew = GmailCrew()
                        gmail_inputs = {"body": meeting_minutes_str}
                        result = gmail_crew.crew().kickoff(gmail_inputs)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Complete!")
                        
                        # Display results
                        st.success("Meeting minutes generated and email draft created successfully!")
                        
                        # Show transcription
                        with st.expander("📄 View Transcription", expanded=False):
                            st.text_area("Transcription", full_transcription, height=200)
                        
                        # Show meeting minutes
                        with st.expander("📋 View Meeting Minutes", expanded=True):
                            st.markdown(meeting_minutes_str)
                        
                        # Show email result
                        with st.expander("📧 Email Status", expanded=False):
                            st.info(f"Email draft result: {str(result)}")
                            st.success(f"Check your Gmail drafts folder for the email to: {recipient}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.error("Please check your configuration and try again.")

with col2:
    st.header("📋 Quick Info")
    
    st.info("""
    **How it works:**
    1. Upload audio file
    2. Audio gets transcribed
    3. Meeting minutes generated
    4. Email draft created
    
    **Requirements:**
    - OpenAI API key
    - Gmail credentials
    - Email configuration
    """)
    
    st.header("🔧 Setup")
    
    if st.button("📖 View Setup Guide"):
        st.markdown("""
        **Setup Steps:**
        
        1. **Environment Variables** (.env file):
        ```
        OPENAI_API_KEY=your_openai_key
        GMAIL_SENDER=your_email@gmail.com
        GMAIL_RECIPIENT=recipient@gmail.com
        AGENTOPS_API_KEY=your_agentops_key
        ```
        
        2. **Gmail Setup**:
        - Download credentials.json from Google Cloud Console
        - Place in: `src/meeting_minutes/crews/gmailcrew/tools/`
        
        3. **Install Dependencies**:
        ```bash
        pip install streamlit openai crewai pydub
        ```
        """)

# Footer
st.divider()
st.markdown("---")
st.markdown("Built with ❤️ CoinCade") 