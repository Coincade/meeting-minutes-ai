#!/usr/bin/env python
# SQLite compatibility fix
import sys
import warnings

# Suppress SQLite version warnings
warnings.filterwarnings("ignore", message=".*sqlite3.*")
warnings.filterwarnings("ignore", message=".*SQLite.*")

# Try to import and apply SQLite patch
try:
    from sqlite_patch import patch_sqlite_version
    patch_sqlite_version()
except ImportError:
    pass

import os
from datetime import datetime
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path

try:
    from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
    from crews.gmailcrew.gmailcrew import GmailCrew
except ImportError:
    # Fallback to import helper
    from import_helper import import_crews
    MeetingMinutesCrew, GmailCrew = import_crews()

import agentops
from dotenv import load_dotenv

# Fix Unicode encoding issues on Windows
if sys.platform == "win32":
    try:
        import codecs
        if hasattr(sys.stdout, 'detach'):
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except Exception:
        # If encoding fix fails, continue without it
        pass

load_dotenv()

client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        audio_path = str(SCRIPT_DIR / "EarningsCall.wav")
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path, format="wav")
        
        # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")

    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating Meeting Minutes")
        # result = (
        #     MeetingMinutesCrew()
        #     .crew()
        #     .kickoff(inputs={"transcript": self.state.transcript})
        # )


        crew = MeetingMinutesCrew()

        inputs = {
            "transcript": self.state.transcript
        }


        meeting_minutes = crew.crew().kickoff(inputs)
        # Convert CrewOutput to string if needed
        if hasattr(meeting_minutes, 'raw'):
            self.state.meeting_minutes = str(meeting_minutes.raw)
        else:
            self.state.meeting_minutes = str(meeting_minutes)

    @listen(generate_meeting_minutes)
    def create_meeting_minutes_draft(self):
        print("Creating Meeting Minutes Email Draft")
        
        # Get email configuration
        sender = os.getenv("GMAIL_SENDER")
        recipient = os.getenv("GMAIL_RECIPIENT")
        
        current_date = datetime.now().strftime("%B %d, %Y")
        print(f"Email Configuration:")
        print(f"  From: {sender}")
        print(f"  To: {recipient}")
        print(f"  Subject: Meeting Minutes - {current_date}")
        
        if not sender or not recipient:
            print("✗ ERROR: Missing email configuration!")
            print("Please set GMAIL_SENDER and GMAIL_RECIPIENT environment variables")
            return
        
        crew = GmailCrew()
        inputs = {
            "body": str(self.state.meeting_minutes)
        }
        
        print("Creating email draft...")
        result = crew.crew().kickoff(inputs)
        result_str = str(result)
        print(f"Draft Result: {result_str}")
        
        if "successfully" in result_str.lower():
            print("✓ Email draft created successfully!")
            print(f"Check your Gmail drafts folder for the meeting minutes draft.")
            print(f"The draft will be sent to: {recipient}")
        else:
            print("✗ Email draft creation failed!")
            print("Check the error message above for details.")

def kickoff():

    try:
        session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
        print("AgentOps initialized successfully")
    except Exception as e:
        print(f"Warning: AgentOps initialization failed: {e}")
        print("Continuing without AgentOps tracing...")
        session = None
    
    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.plot()
    meeting_minutes_flow.kickoff()
    
    if session:
        try:
            agentops.end_trace()
            print("AgentOps trace ended successfully")
        except Exception as e:
            print(f"Warning: Failed to end AgentOps trace: {e}")

if __name__ == "__main__":
    kickoff()