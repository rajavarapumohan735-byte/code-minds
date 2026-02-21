#!/bin/bash

echo "Starting ResearchHub AI Development Environment"
echo "=============================================="
echo ""

check_backend_env() {
    if [ ! -f "backend/.env" ]; then
        echo "❌ Backend .env file not found!"
        echo "Please create backend/.env with your configuration."
        echo "See backend/.env.example for reference."
        exit 1
    fi
}

check_frontend_env() {
    if [ ! -f ".env" ]; then
        echo "⚠️  Frontend .env not found, creating one..."
        echo "VITE_API_URL=http://localhost:8000" > .env
        echo "✅ Created .env file"
    fi
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3.9+"
        exit 1
    fi
}

check_node() {
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
}

echo "Checking prerequisites..."
check_python
check_node
check_backend_env
check_frontend_env

echo "✅ All prerequisites met!"
echo ""

echo "Installing frontend dependencies..."
npm install
echo ""

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..
echo ""

echo "Starting services..."
echo "Backend will run on http://localhost:8000"
echo "Frontend will run on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..
npm run dev &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID
