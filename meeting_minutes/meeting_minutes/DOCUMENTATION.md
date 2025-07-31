# Crew AI Meeting Minutes Project: Build & Flow Documentation

## Overview
This documentation summarizes all the key steps, commands, and code changes made to build the meeting minutes automation project. It covers the initial setup, audio transcription, meeting minutes generation, and automated draft email creation using CrewAI, OpenAI, and Gmail API integration.

---

## 1. **Project Initialization**
- **Directory Structure**: The project is organized with clear separation for source code, configuration, and audio files.
- **Key Directories/Files**:
  - `src/meeting_minutes/`: Main Python source code
  - `crews/meeting_minutes_crew/`: Handles meeting minutes summarization
  - `crews/gmailcrew/`: Handles Gmail draft creation
  - `crews/gmailcrew/config/`: YAML config for agents and tasks
  - `EarningsCall.wav` and `chunk_*.wav`: Audio files for transcription

---

## 2. **Environment Setup**
- **Python Packages**: Installed via `pip` (not shown here, but required):
  - `crewai`, `openai`, `pydub`, `pydantic`, `python-dotenv`, `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`, etc.
- **.env File**: Stores sensitive environment variables:
  - `GMAIL_SENDER` and `GMAIL_RECIPIENT` for Gmail API
  - `OPENAI_API_KEY` for OpenAI access
- **Google API Credentials**: `credentials.json` placed in the Gmail tools directory for OAuth2 authentication.

---

## 3. **Audio Transcription Flow**
- **File**: `main.py`
- **Key Steps**:
  - Loads and chunks the audio file (`EarningsCall.wav`) using `pydub`.
  - Transcribes each chunk using OpenAI Whisper API.
  - Aggregates the transcript for further processing.
- **Importance**: Automates the conversion of meeting audio into text, which is the foundation for all downstream processing.

---

## 4. **Meeting Minutes Generation**
- **File**: `main.py` and `crews/meeting_minutes_crew/meeting_minutes_crew.py`
- **Key Steps**:
  - Passes the transcript to the `MeetingMinutesCrew`.
  - Uses CrewAI agents to summarize, extract action items, and analyze sentiment.
  - Outputs are written to `summary.txt`, `action_items.txt`, and `sentiment.txt`.
- **Importance**: Provides structured, actionable meeting documentation automatically.

---

## 5. **Gmail Draft Creation**
- **Files**: `main.py`, `crews/gmailcrew/gmailcrew.py`, `crews/gmailcrew/tools/gmail_tool.py`, `crews/gmailcrew/tools/gmail_utility.py`
- **Key Steps**:
  - After generating meeting minutes, the flow triggers the Gmail draft creation.
  - The `GmailCrew` agent uses the `GmailTool` to authenticate with Gmail and create a draft email with the meeting minutes as the body.
  - The draft is created in the sender's Gmail account, ready for review and sending.
- **Importance**: Automates the distribution of meeting minutes, saving manual effort and ensuring timely communication.

---

## 6. **Configuration Files**
- **agents.yaml** and **tasks.yaml** in `crews/gmailcrew/config/`:
  - Define the agent (`gmail_draft_agent`) and task (`gmail_draft_task`) for the Gmail crew.
  - Ensures CrewAI knows how to instantiate and connect the right logic for email drafting.
- **Importance**: Decouples logic from code, making it easy to update agent/task behavior without code changes.

---

## 7. **Key Code Fixes and Their Importance**
- **YAML Cleanup**: Removed old 'researcher' and 'reporting_analyst' references to prevent `KeyError` and ensure correct agent/task mapping.
- **CrewOutput Handling**: Converted CrewAI outputs to string before passing to Gmail agent, preventing type errors.
- **Result Handling**: Always convert results to string before using `.lower()` or printing, to avoid attribute errors with CrewOutput objects.
- **Minimal Changes Principle**: All fixes were made with minimal disruption to the original code structure, following best practices and the referenced YouTube tutorial.

---

## 8. **How the Flow Works (End-to-End)**
1. **Transcribe Meeting**: Audio is chunked and transcribed.
2. **Generate Minutes**: Transcript is summarized, action items and sentiment are extracted.
3. **Create Email Draft**: Meeting minutes are used as the body for a Gmail draft, created automatically.
4. **Review & Send**: User reviews the draft in Gmail and sends it to the intended recipient.

---

## 9. **Troubleshooting & Lessons Learned**
- **Always check YAML config for old agent/task names** if you see KeyError.
- **Convert all CrewAI outputs to string** before using in downstream tasks.
- **Environment variables and credentials** must be set for Gmail API to work.
- **Minimal, targeted changes** are best for debugging and maintaining code.

---

## 10. **References**
- [YouTube Tutorial Reference](https://www.youtube.com/watch?v=ONKOXwucLvE&t=4894s)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Google Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

---

## 11. **Final Notes**
- This documentation should serve as a clear reference for the build, flow, and troubleshooting of your CrewAI meeting minutes automation project.
- For any future changes, always update this file to keep your workflow transparent and maintainable. 