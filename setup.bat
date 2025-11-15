@echo off
REM Sacha Advisor - Quick Start Script for Windows

echo.
echo 🚀 Sacha Advisor - Quick Start Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed
echo.

REM Setup backend
echo 📦 Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt >nul 2>&1
echo ✅ Backend dependencies installed

REM Create .env if it doesn't exist
if not exist ".env" (
    copy .env.example .env
    echo ⚠️  .env file created. Please add your OpenAI API key.
)

cd ..

REM Setup frontend
echo.
echo 📦 Setting up Frontend...
cd frontend

REM Install dependencies
if not exist "node_modules" (
    npm install --silent
    echo ✅ Frontend dependencies installed
)

cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Add your OpenAI API key to: backend\.env
echo 2. In one terminal, run: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo 3. In another terminal, run: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:5173 in your browser
echo.
echo 🎉 Enjoy using Sacha Advisor!
echo.
pause
