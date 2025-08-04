#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Document Processing System (Development) ---"

# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it to continue."
    exit 1
fi

# Create and activate a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies quietly
echo "Installing dependencies from requirements.txt..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p documents
mkdir -p vector_store

echo "--------------------------------------------------------"
echo "✅ Setup complete. Starting FastAPI server with auto-reload..."
echo "API will be available at http://127.0.0.1:8000"
echo "View interactive API docs at http://127.0.0.1:8000/docs"
echo "Press CTRL+C to stop the server."
echo "--------------------------------------------------------"

# Run the FastAPI application with auto-reload for development
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
