#!/bin/bash

echo "--- Starting Document Processing System ---"

# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it to continue."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -q -r requirements.txt

# Create necessary directories if they don't exist
mkdir -p documents
mkdir -p vector_store

echo "--------------------------------------------------------"
echo "Setup complete. Starting FastAPI server..."
echo "Place your PDF and DOCX files in the 'documents' folder."
echo "API will be available at http://127.0.0.1:8000"
echo "View interactive API docs at http://127.0.0.1:8000/docs"
echo "Press CTRL+C to stop the server."
echo "--------------------------------------------------------"

# Run the FastAPI application
uvicorn app:app --host 0.0.0.0 --port 8000