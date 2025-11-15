#!/bin/bash

echo "🚀 Sacha Advisor - Quick Start Script"
echo "======================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9+."
    exit 1
fi

echo "✅ Node.js and Python are installed"
echo ""

# Setup backend
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --quiet
echo "✅ Backend dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  .env file created. Please add your OpenAI API key."
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo "✅ Frontend dependencies installed"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to: backend/.env"
echo "2. In one terminal, run: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "3. In another terminal, run: cd frontend && npm run dev"
echo "4. Open http://localhost:5173 in your browser"
echo ""
echo "🎉 Enjoy using Sacha Advisor!"
