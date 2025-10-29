#!/bin/bash

# Resume Analyzer Backend Startup Script

echo "🚀 Starting Resume Analyzer Backend..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    touch venv/.dependencies_installed
    echo "✅ Dependencies installed!"
else
    echo "✅ Dependencies already installed"
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Run the Flask application
echo "🌟 Starting Flask server on http://localhost:5000"
python app.py






