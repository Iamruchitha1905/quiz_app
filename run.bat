@echo off
echo Setting up Quiz Application...

:: Backend Setup
echo [1/4] Setting up Backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
start "Quiz Backend" cmd /k "python main.py"
cd ..

:: Frontend Setup
echo [2/4] Setting up Frontend...
cd frontend
if not exist node_modules (
    npm install
)
echo [3/4] Starting Frontend...
start "Quiz Frontend" cmd /k "npm run dev"
cd ..

echo [4/4] DONE!
echo Backend is running on http://localhost:8000
echo Frontend is running on http://localhost:5173
echo.
echo Opening browser...
start http://localhost:5173
pause
