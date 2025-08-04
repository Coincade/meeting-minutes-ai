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

1. **Install SQLite compatibility first:**
   ```bash
   pip install pysqlite3-binary>=0.5.2
   ```

2. **Install the package:**
   ```bash
   pip install -e .
   ```

3. **Install additional requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Using UV (Alternative)

If you have UV installed:

```bash
pip install uv
uv pip install pysqlite3-binary>=0.5.2
uv pip install -e .
uv pip install -r requirements.txt
```

## Configuration

1. **Create a `.env` file** in the project root with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **For Gmail integration** (optional), add:
   ```env
   GMAIL_CLIENT_ID=your_gmail_client_id
   GMAIL_CLIENT_SECRET=your_gmail_client_secret
   GMAIL_REFRESH_TOKEN=your_gmail_refresh_token
   ```

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

## Troubleshooting

### SQLite Version Issues

If you encounter SQLite version errors, the installation script should handle this automatically. If issues persist:

1. Ensure `pysqlite3-binary` is installed:
   ```bash
   pip install pysqlite3-binary>=0.5.2
   ```

2. The application includes SQLite compatibility fixes in the code

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
