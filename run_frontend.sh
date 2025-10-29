#!/bin/bash

# Resume Analyzer Frontend Startup Script

echo "🚀 Starting Resume Analyzer Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm packages..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Run the development server
echo "🌟 Starting Vite dev server on http://localhost:5173"
npm run dev






