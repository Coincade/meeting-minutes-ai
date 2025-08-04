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

# Custom CSS for modern UI with softer colors
st.markdown("""
<style>
    /* Modern styling with softer colors */
    .main-header {
        background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: #f7fafc;
        text-align: center;
    }
    
    .status-card {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #48bb78;
        margin: 0.5rem 0;
        color: #2d3748;
    }
    
    .error-card {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f56565;
        margin: 0.5rem 0;
        color: #2d3748;
    }
    
    .upload-area {
        border: 2px dashed #718096;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f7fafc;
        transition: all 0.3s ease;
        color: #4a5568;
    }
    
    .upload-area:hover {
        border-color: #4a5568;
        background: #edf2f7;
    }
    
    .progress-container {
        background: #f7fafc;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .result-card {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #2d3748;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar text color */
    .css-1d391kg .stMarkdown {
        color: white !important;
    }
    
    /* Sidebar input styling */
    .css-1d391kg .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .css-1d391kg .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Sidebar button styling */
    .css-1d391kg .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%);
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        color: #f7fafc;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        background: linear-gradient(90deg, #2d3748 0%, #1a202c 100%);
    }
    
    .file-info {
        background: #ebf8ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #bee3f8;
        color: #2c5282;
    }
    
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        position: relative;
    }
    
    .step {
        background: #4a5568;
        color: #f7fafc;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        position: relative;
        z-index: 2;
    }
    
    .step.active {
        background: #48bb78;
        transform: scale(1.1);
    }
    
    .step.completed {
        background: #48bb78;
    }
    
    .step-line {
        position: absolute;
        top: 20px;
        left: 20px;
        right: 20px;
        height: 2px;
        background: #e2e8f0;
        z-index: 1;
    }
    
    /* Softer text colors */
    .stMarkdown {
        color: #2d3748;
    }
    
    /* Softer background for main content */
    .main .block-container {
        background-color: #f7fafc;
    }
    
    /* Softer sidebar */
    .css-1d391kg {
        background-color: #f7fafc;
    }
    
    /* Meeting minutes styling */
    .meeting-minutes-content {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
        color: #1e293b;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .meeting-minutes-content h1,
    .meeting-minutes-content h2,
    .meeting-minutes-content h3,
    .meeting-minutes-content h4,
    .meeting-minutes-content h5,
    .meeting-minutes-content h6 {
        color: #1e40af;
        border-bottom: 2px solid #bfdbfe;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .meeting-minutes-content p {
        color: #374151;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .meeting-minutes-content ul,
    .meeting-minutes-content ol {
        color: #374151;
        margin-left: 1.5rem;
    }
    
    .meeting-minutes-content li {
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .meeting-minutes-content strong,
    .meeting-minutes-content b {
        color: #dc2626;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="Meeting Minutes Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main header with gradient
st.markdown("""
<div class="main-header">
    <h1>🎙️ Meeting Minutes Generator</h1>
    <p>Transform your audio meetings into professional minutes with AI-powered transcription and automated email drafting</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with modern design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.1); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);">
        <h2 style="color: white; margin: 0;">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Email settings with better styling
    st.markdown("### 📧 Email Settings")
    
    sender = st.text_input(
        "📤 Sender Email", 
        value=os.getenv("GMAIL_SENDER", ""),
        help="Your Gmail address for sending meeting minutes",
        placeholder="your.email@gmail.com"
    )
    
    recipient = st.text_input(
        "📥 Recipient Email", 
        value=os.getenv("GMAIL_RECIPIENT", ""),
        help="Email address to receive meeting minutes",
        placeholder="recipient@company.com"
    )
    
    # Save button with better styling
    if st.button("💾 Save Configuration", use_container_width=True):
        os.environ["GMAIL_SENDER"] = sender
        os.environ["GMAIL_RECIPIENT"] = recipient
        st.success("✅ Configuration saved successfully!")
     
    st.divider()
    
    # Status dashboard
    st.markdown("### 📊 System Status")
    
    # Email configuration status
    if os.getenv("GMAIL_SENDER") and os.getenv("GMAIL_RECIPIENT"):
        st.markdown("""
        <div class="status-card">
            <strong>✅ Email Configuration</strong><br>
            Ready to send meeting minutes
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-card">
            <strong>❌ Email Configuration</strong><br>
            Please configure sender and recipient
        </div>
        """, unsafe_allow_html=True)
    
    # Gmail credentials status
    if os.path.exists("src/meeting_minutes/crews/gmailcrew/tools/credentials.json"):
        st.markdown("""
        <div class="status-card">
            <strong>✅ Gmail Credentials</strong><br>
            Authentication ready
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-card">
            <strong>❌ Gmail Credentials</strong><br>
            Missing credentials.json
        </div>
        """, unsafe_allow_html=True)
    
    # OpenAI API status
    if os.getenv("OPENAI_API_KEY"):
        st.markdown("""
        <div class="status-card">
            <strong>✅ OpenAI API</strong><br>
            Transcription ready
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-card">
            <strong>❌ OpenAI API</strong><br>
            Missing API key
        </div>
        """, unsafe_allow_html=True)

# Main content area - centered upload section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # File upload section with modern design - centered
    st.markdown("### 📁 Upload Meeting Audio")
    
    # Custom upload area
    uploaded_file = st.file_uploader(
        "Choose an audio file or drag and drop here",
        type=['wav', 'mp3', 'm4a', 'flac'],
        help="Supported formats: WAV, MP3, M4A, FLAC (Max 200MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Enhanced file info display
        file_size_mb = uploaded_file.size / 1024 / 1024
        st.markdown(f"""
        <div class="file-info">
            <h4>📄 File Details</h4>
            <p><strong>Name:</strong> {uploaded_file.name}</p>
            <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>
            <p><strong>Type:</strong> {uploaded_file.type or 'Audio'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Process button with better styling
        if st.button("🚀 Generate Meeting Minutes", type="primary", use_container_width=True):
            if not sender or not recipient:
                st.error("⚠️ Please configure email settings in the sidebar first!")
            else:
                # Single step indicator and progress container
                step_container = st.empty()
                progress_container = st.container()
                
                with progress_container:
                    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                try:
                    # Function to update single step indicator
                    def update_step_indicator(current_step):
                        steps = []
                        for i in range(1, 5):
                            if current_step > 4:  # All completed
                                steps.append(f'<div class="step completed">{i}</div>')
                            elif i < current_step:
                                steps.append(f'<div class="step completed">{i}</div>')
                            elif i == current_step:
                                steps.append(f'<div class="step active">{i}</div>')
                            else:
                                steps.append(f'<div class="step">{i}</div>')
                        
                        step_html = f"""
                        <div class="step-indicator">
                            <div class="step-line"></div>
                            {''.join(steps)}
                        </div>
                        """
                        step_container.markdown(step_html, unsafe_allow_html=True)
                    
                    # Step 1: Save uploaded file
                    update_step_indicator(1)
                    status_text.markdown("**Step 1:** 📁 Processing audio file...")
                    progress_bar.progress(10)
                    
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                        with open(temp_audio_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Step 2: Transcribe audio
                        update_step_indicator(2)
                        status_text.markdown("**Step 2:** 🎙️ Transcribing audio with OpenAI Whisper...")
                        progress_bar.progress(30)
                        
                        from openai import OpenAI
                        from pydub import AudioSegment
                        from pydub.utils import make_chunks
                        
                        client = OpenAI()
                        
                        # Load and chunk audio
                        audio = AudioSegment.from_file(temp_audio_path)
                        chunk_length_ms = 60000
                        chunks = make_chunks(audio, chunk_length_ms)
                        
                        # Transcribe chunks with progress
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
                        update_step_indicator(3)
                        status_text.markdown("**Step 3:** 📝 Generating meeting minutes with CrewAI...")
                        progress_bar.progress(70)
                        
                        crew = MeetingMinutesCrew()
                        inputs = {"transcript": full_transcription}
                        meeting_minutes = crew.crew().kickoff(inputs)
                        
                        if hasattr(meeting_minutes, 'raw'):
                            meeting_minutes_str = str(meeting_minutes.raw)
                        else:
                            meeting_minutes_str = str(meeting_minutes)
                        
                        progress_bar.progress(85)
                        
                        # Step 4: Create email draft
                        update_step_indicator(4)
                        status_text.markdown("**Step 4:** 📧 Creating email draft...")
                        progress_bar.progress(90)
                        
                        gmail_crew = GmailCrew()
                        gmail_inputs = {"body": meeting_minutes_str}
                        result = gmail_crew.crew().kickoff(gmail_inputs)
                        
                        progress_bar.progress(100)
                        # Update step indicator to show all completed
                        update_step_indicator(5)  # This will show all steps as completed
                        status_text.markdown("**✅ Complete!** Meeting minutes generated and email draft created!")
                        
                        # Success message
                        st.success("🎉 **Success!** Your meeting minutes have been generated and an email draft has been created!")
                        
                        # Results in expandable cards
                        with st.expander("📄 View Raw Transcription", expanded=False):
                            st.text_area("Transcription", full_transcription, height=200, disabled=True)
                        
                        with st.expander("📋 View Generated Meeting Minutes", expanded=True):
                            st.markdown(f"""
                            <div class="meeting-minutes-content">
                                {meeting_minutes_str}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with st.expander("📧 Email Status", expanded=False):
                            st.info(f"**Email Draft Result:** {str(result)}")
                            st.success(f"📬 Check your Gmail drafts folder for the email to: **{recipient}**")
                
                except Exception as e:
                    st.error(f"❌ **Error occurred:** {str(e)}")
                    st.error("Please check your configuration and try again.")

 