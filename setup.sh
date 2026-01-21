#!/bin/bash
# Clinical AI Multi-Agent System - Setup and Deployment Script
# This script automates project setup, testing, and deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed"
        exit 1
    fi

    # Check Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version 2>&1 | awk '{print $3}' | tr -d ',')
        print_success "Docker found: $DOCKER_VERSION"
    else
        print_warning "Docker is not installed (optional for containerization)"
    fi

    # Check Git
    if command -v git &> /dev/null; then
        print_success "Git is installed"
    else
        print_warning "Git is not installed (optional)"
    fi
}

# Setup Python environment
setup_environment() {
    print_header "Setting Up Python Environment"

    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_warning "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi

    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"

    # Upgrade pip
    python3 -m pip install --upgrade pip
    print_success "pip upgraded"

    # Install requirements
    if [ -f "requirements.txt" ]; then
        print_warning "Installing dependencies..."
        pip install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Setup configuration
setup_configuration() {
    print_header "Setting Up Configuration"

    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating template..."
        cat > .env.template << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# Qdrant Configuration
QDRANT_ENDPOINT=https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_CLUSTER_ID=your-cluster-id

# Google Cloud Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
EOF
        print_success "Created .env.template - please fill in your credentials"
        print_warning "Copy .env.template to .env and update with your API keys"
    else
        print_success ".env file found"
    fi

    # Verify config/settings.py
    if [ -f "config/settings.py" ]; then
        print_success "Configuration file found: config/settings.py"
    else
        print_warning "Configuration file not found"
    fi
}

# Generate test data
generate_test_data() {
    print_header "Generating Test Data"

    print_warning "Creating synthetic medical test data for 10 patients..."
    python3 tests/test_data_generator.py

    if [ $? -eq 0 ]; then
        print_success "Test data generated successfully"
    else
        print_error "Failed to generate test data"
        exit 1
    fi
}

# Run tests
run_tests() {
    print_header "Running Integration Tests"

    print_warning "Running comprehensive test suite..."
    python3 -m pytest tests/test_integration.py -v

    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_warning "Some tests failed - review output above"
    fi
}

# Start development server
start_dev_server() {
    print_header "Starting Development Server"

    print_warning "Starting FastAPI development server..."
    print_success "API will be available at: http://localhost:8000"
    print_success "Documentation at: http://localhost:8000/docs"
    print_success ""

    python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
}

# Build Docker image
build_docker_image() {
    print_header "Building Docker Image"

    if command -v docker &> /dev/null; then
        print_warning "Building Docker image..."
        docker build -t clinical-ai:latest .
        print_success "Docker image built: clinical-ai:latest"
    else
        print_error "Docker is not installed"
        exit 1
    fi
}

# Deploy to GCP
deploy_to_gcp() {
    print_header "Preparing GCP Deployment"

    if command -v gcloud &> /dev/null; then
        print_warning "You can now deploy to GCP using:"
        echo -e "${GREEN}gcloud run deploy clinical-ai \\${NC}"
        echo -e "${GREEN}    --image gcr.io/\${PROJECT_ID}/clinical-ai:latest \\${NC}"
        echo -e "${GREEN}    --platform managed \\${NC}"
        echo -e "${GREEN}    --region us-central1${NC}"
    else
        print_warning "gcloud CLI not installed - see README.md for GCP deployment steps"
    fi
}

# Display menu
show_menu() {
    print_header "Clinical AI Multi-Agent System - Setup Wizard"
    echo "1) Check Prerequisites"
    echo "2) Setup Python Environment"
    echo "3) Setup Configuration"
    echo "4) Generate Test Data"
    echo "5) Run Integration Tests"
    echo "6) Start Development Server"
    echo "7) Build Docker Image"
    echo "8) Setup GCP Deployment"
    echo "9) Run Full Setup (1-6)"
    echo "10) Exit"
    echo ""
}

# Main menu loop
main() {
    while true; do
        show_menu
        read -p "Select an option [1-10]: " choice

        case $choice in
            1) check_prerequisites ;;
            2) setup_environment ;;
            3) setup_configuration ;;
            4) generate_test_data ;;
            5) run_tests ;;
            6) start_dev_server ;;
            7) build_docker_image ;;
            8) deploy_to_gcp ;;
            9)
                check_prerequisites
                setup_environment
                setup_configuration
                generate_test_data
                run_tests
                print_header "Setup Complete!"
                print_success "You can now start the development server with: python3 -m uvicorn api.main:app --reload"
                ;;
            10)
                print_success "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                ;;
        esac
    done
}

# Check if running with arguments
if [ $# -eq 0 ]; then
    main
else
    case $1 in
        check) check_prerequisites ;;
        setup) setup_environment && setup_configuration ;;
        test) generate_test_data && run_tests ;;
        dev) start_dev_server ;;
        docker) build_docker_image ;;
        gcp) deploy_to_gcp ;;
        full) check_prerequisites && setup_environment && setup_configuration && generate_test_data && run_tests ;;
        *)
            print_error "Unknown command: $1"
            echo "Usage: ./setup.sh [check|setup|test|dev|docker|gcp|full]"
            exit 1
            ;;
    esac
fi
