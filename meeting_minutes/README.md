# Meeting Minutes AI

Welcome to the Meeting Minutes AI project, powered by [crewAI](https://crewai.com). This application automatically generates meeting minutes from audio recordings using a multi-agent AI system.

## Features

- 🎤 Audio transcription using OpenAI Whisper
- 📝 Automatic meeting minutes generation
- 📧 Gmail integration for email processing
- 🎨 Modern Streamlit web interface
- 🤖 Multi-agent AI collaboration

## Prerequisites

- Python >=3.10 <3.14
- OpenAI API key
- (Optional) Gmail API credentials for email processing

## SQLite Compatibility

This application uses ChromaDB which requires SQLite >= 3.35.0. If you encounter SQLite version errors:

### Automatic Fix (Recommended)
The application includes automatic SQLite compatibility patches that will:
- Install `pysqlite3-binary` for newer SQLite support
- Apply environment variable patches
- Suppress compatibility warnings

### Manual Fix
If automatic patches don't work:

1. **Install ChromaDB with specific version:**
   ```bash
   pip install chromadb>=0.4.0,<0.5.0
   ```

2. **Set environment variables:**
   
   **For Linux/macOS:**
   ```bash
   export CHROMA_SILENCE_DEPRECATION_WARNINGS=1
   export TOKENIZERS_PARALLELISM=false
   export CHROMA_DB_IMPL=duckdb+parquet
   ```
   
   **For Windows PowerShell:**
   ```powershell
   .\setup_windows.ps1
   ```
   
   **For Windows Command Prompt:**
   ```cmd
   set CHROMA_SILENCE_DEPRECATION_WARNINGS=1
   set TOKENIZERS_PARALLELISM=false
   set CHROMA_DB_IMPL=duckdb+parquet
   ```

3. **Upgrade system SQLite (if possible):**
   - **Ubuntu/Debian:** `sudo apt update && sudo apt install sqlite3`
   - **macOS:** `brew install sqlite3`
   - **Windows:** Download from [SQLite website](https://www.sqlite.org/download.html)

## Installation

### Method 1: Automated Installation (Recommended)

Run the automated installation script:

```bash
python install_dependencies.py
```

This script will:
- Install SQLite compatibility packages
- Set up all dependencies
- Handle common installation issues

### Method 2: Manual Installation

If you prefer manual installation:

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Install additional requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Using UV (Alternative)

If you have UV installed:

```bash
pip install uv
uv pip install -e .
uv pip install -r requirements.txt
```

## Configuration

### Environment Variables

1. **Create a `.env` file** in the project root with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GMAIL_SENDER=your-production-email@gmail.com
   GMAIL_RECIPIENT=recipient-email@domain.com
   ```

### Gmail API Setup (Optional)

For Gmail integration, you need to set up OAuth2 credentials:

1. **Get Google Cloud OAuth2 credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the `credentials.json` file

2. **Place credentials file:**
   - Put `credentials.json` in `src/meeting_minutes/crews/gmailcrew/tools/`
   - The application will automatically authenticate on first run

3. **Set environment variables:**
   ```env
   GMAIL_SENDER=your-production-email@gmail.com
   GMAIL_RECIPIENT=recipient-email@domain.com
   ```

**Note:** For production deployment, use your production email addresses, not test credentials.

## Running the Application

### Streamlit Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

This launches a modern web interface where you can:
- Upload audio files
- Generate meeting minutes
- View results in real-time

### Command Line Interface

```bash
python src/meeting_minutes/main.py
```

This runs the core meeting minutes generation workflow.

## Deployment

### Production Deployment

For production deployment, follow these steps:

1. **Environment Setup:**
   - Copy `env.example` to `.env`
   - Update with your production credentials
   - Set `GMAIL_SENDER` and `GMAIL_RECIPIENT` to production email addresses

2. **Gmail Credentials:**
   - Place your production `credentials.json` in `src/meeting_minutes/crews/gmailcrew/tools/`
   - The application will authenticate automatically on first run

3. **Security Notes:**
   - Never commit `.env` files or `credentials.json` to version control
   - Use environment variables in your deployment platform
   - Keep `token.json` secure (contains OAuth tokens)

4. **Deployment Platforms:**
   - **Streamlit Cloud:** Upload to GitHub and connect
   - **Heroku:** Use `Procfile` with `streamlit run streamlit_app.py`
   - **Docker:** Use the provided Dockerfile (if available)

### Environment Variables for Production

```env
# Required
OPENAI_API_KEY=your-production-openai-key

# Gmail (optional)
GMAIL_SENDER=your-production-email@gmail.com
GMAIL_RECIPIENT=recipient-email@domain.com
```

## Troubleshooting

### SQLite Version Issues

If you encounter SQLite version errors, the application includes SQLite compatibility fixes in the code. The installation script should handle this automatically.

### Import Errors

If you see import errors:
1. Ensure you're in the project root directory
2. Run `python install_dependencies.py` to fix dependency issues
3. Check that all requirements are installed

## Project Structure

```
meeting_minutes/
├── src/meeting_minutes/
│   ├── crews/                    # AI crew definitions
│   │   ├── meeting_minutes_crew/ # Meeting minutes generation
│   │   └── gmailcrew/           # Gmail processing
│   ├── tools/                   # Custom tools
│   └── main.py                  # CLI entry point
├── streamlit_app.py             # Web interface
├── install_dependencies.py      # Installation script
└── requirements.txt             # Dependencies
```

## Support

For support, questions, or feedback:

- Visit our [documentation](https://docs.crewai.com)
- Reach out through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)

Let's create amazing meeting minutes together with the power of AI! 🚀
