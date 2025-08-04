# PowerShell script to set environment variables for Meeting Minutes AI
# Run this script before starting the application

Write-Host "🔧 Setting up environment variables for Meeting Minutes AI..." -ForegroundColor Green

# Set environment variables
$env:CHROMA_SILENCE_DEPRECATION_WARNINGS = "1"
$env:TOKENIZERS_PARALLELISM = "false"
$env:CHROMA_DB_IMPL = "duckdb+parquet"

Write-Host "✅ Environment variables set successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the application with:" -ForegroundColor Yellow
Write-Host "  streamlit run streamlit_app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or test the setup with:" -ForegroundColor Yellow
Write-Host "  python quick_test.py" -ForegroundColor Cyan 