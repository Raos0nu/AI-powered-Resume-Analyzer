#!/bin/bash

# AI-Powered Resume Analyzer - Startup Script
# This script starts both the backend server and opens the frontend

echo "🚀 Starting AI-Powered Resume Analyzer..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv"
    echo "Then activate it and install dependencies: pip install -r backend/requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Start backend server in background
echo "🖥️  Starting backend server on http://localhost:5000..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start frontend server
echo "🌐 Starting frontend server on http://localhost:8080..."
cd frontend
python -m http.server 8080 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📊 Backend API: http://localhost:5000"
echo "🌐 Frontend UI: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all servers..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All servers stopped. Goodbye!"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait

