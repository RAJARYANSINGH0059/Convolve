# Clinical AI Multi-Agent System - Windows Setup Script
# PowerShell script for automated setup on Windows

param(
    [string]$Action = "menu"
)

# Color functions
function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host " $Message" -ForegroundColor Green
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host " $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host " $Message" -ForegroundColor Yellow
}

# Check prerequisites
function Check-Prerequisites {
    Write-Header "Checking Prerequisites"

    # Check Python
    $pythonExists = (Get-Command python -ErrorAction SilentlyContinue) -ne $null
    if ($pythonExists) {
        $pythonVersion = (python --version 2>&1)
        Write-Success "Python found: $pythonVersion"
    } else {
        Write-ErrorMsg "Python is not installed"
        Write-Warning "Download from: https://www.python.org/downloads/"
        return $false
    }

    # Check Docker
    $dockerExists = (Get-Command docker -ErrorAction SilentlyContinue) -ne $null
    if ($dockerExists) {
        $dockerVersion = (docker --version)
        Write-Success "Docker found: $dockerVersion"
    } else {
        Write-Warning "Docker is not installed (optional for development)"
        Write-Warning "Download from: https://www.docker.com/products/docker-desktop"
    }

    # Check Git
    $gitExists = (Get-Command git -ErrorAction SilentlyContinue) -ne $null
    if ($gitExists) {
        Write-Success "Git found"
    } else {
        Write-Warning "Git is not installed (optional)"
        Write-Warning "Download from: https://git-scm.com/download/win"
    }

    return $true
}

# Setup Python environment
function Setup-PythonEnvironment {
    Write-Header "Setting Up Python Environment"

    # Create virtual environment
    if (-not (Test-Path "venv")) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
        Write-Success "Virtual environment created"
    } else {
        Write-Success "Virtual environment already exists"
    }

    # Activate virtual environment
    Write-Host "Activating virtual environment..."
    & "venv\Scripts\Activate.ps1"

    # Upgrade pip
    Write-Host "Upgrading pip..."
    python -m pip install --upgrade pip

    # Install requirements
    Write-Host "Installing dependencies..."
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Success "Dependencies installed"
    } else {
        Write-ErrorMsg "requirements.txt not found"
        return $false
    }

    return $true
}

# Setup configuration
function Setup-Configuration {
    Write-Header "Setting Up Configuration"

    # Check if .env exists
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file..."
        Add-Content -Path ".env" -Value "# OpenAI Configuration"
        Add-Content -Path ".env" -Value "OPENAI_API_KEY=your-openai-api-key-here"
        Add-Content -Path ".env" -Value "OPENAI_MODEL=gpt-4-turbo"
        Add-Content -Path ".env" -Value ""
        Add-Content -Path ".env" -Value "# Google Configuration"
        Add-Content -Path ".env" -Value "GOOGLE_API_KEY=your-google-api-key-here"
        Add-Content -Path ".env" -Value "GOOGLE_MODEL_ID=gemini-pro"
        Add-Content -Path ".env" -Value ""
        Add-Content -Path ".env" -Value "# Vertex AI Configuration"
        Add-Content -Path ".env" -Value "VERTEX_PROJECT_ID=your-gcp-project-id"
        Add-Content -Path ".env" -Value "VERTEX_LOCATION=us-central1"
        Add-Content -Path ".env" -Value "VERTEX_MODEL_ID=gemini-1.5-pro"
        Add-Content -Path ".env" -Value ""
        Add-Content -Path ".env" -Value "# Qdrant Configuration"
        Add-Content -Path ".env" -Value "QDRANT_ENDPOINT=https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io"
        Add-Content -Path ".env" -Value "QDRANT_API_KEY=your-qdrant-api-key-here"
        Add-Content -Path ".env" -Value ""
        Add-Content -Path ".env" -Value "# API Configuration"
        Add-Content -Path ".env" -Value "API_HOST=0.0.0.0"
        Add-Content -Path ".env" -Value "API_PORT=8000"
        Write-Success "Created .env file"
        Write-Warning "Please edit .env and add your API keys"
    } else {
        Write-Success ".env file already exists"
    }

    if (Test-Path "config/settings.py") {
        Write-Success "Configuration file found: config/settings.py"
    } else {
        Write-ErrorMsg "Configuration file not found"
    }
}

# Start development server
function Start-DevServer {
    Write-Header "Starting Development Server"

    & "venv\Scripts\Activate.ps1"

    $uvicornExists = (pip show uvicorn) -ne $null
    if (-not $uvicornExists) {
        Write-Host "Installing uvicorn..."
        pip install uvicorn
    }

    Write-Host "Starting FastAPI development server..."
    Write-Host ""
    Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Green
    Write-Host "API documentation at: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server"
    Write-Host ""

    python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
}

function Run-FullSetup {
    Write-Header "Running Full Setup"

    if (-not (Check-Prerequisites)) {
        Write-ErrorMsg "Prerequisites check failed"
        exit 1
    }

    if (-not (Setup-PythonEnvironment)) {
        Write-ErrorMsg "Python environment setup failed"
        exit 1
    }

    Setup-Configuration

    Write-Header "Setup Complete!"
    Write-Host ""
    Write-Success "Clinical AI Multi-Agent System is ready!"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1) Edit .env file with your API keys"
    Write-Host "2) Start development server: python -m uvicorn api.main:app --reload"
    Write-Host "3) Visit dashboard: http://localhost:8000"
    Write-Host ""
}

if ($Action -eq "full") {
    Run-FullSetup
} else {
    Write-ErrorMsg "Unknown action: $Action"
    Write-Host "Usage: .\setup.ps1 -Action full"
    exit 1
}
