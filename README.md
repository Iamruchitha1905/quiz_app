# Full-Stack Quiz Application

A modern, responsive, and interactive quiz application built with FastAPI and React.

## Features
- **Dynamic Quiz**: Fetch questions from SQLite backend.
- **Modern UI**: Clean design inspired by W3Schools but highly polished.
- **Timer**: 15-second countdown per question.
- **Animated Progress Bar**: Visual feedback on quiz completion.
- **Smooth Transitions**: Fade and slide effects between questions.
- **Detailed Results**: Instant scoring and feedback with correct answer highlights.
- **Mobile Responsive**: Works perfectly on all screen sizes.

## Project Structure
- `backend/`: FastAPI application with SQLite database.
- `frontend/`: React application using Vite and Axios.

## Prerequisites
- Python 3.8+
- Node.js 18+

## Quick Start (Windows)

1. **Install Backend Dependencies**:
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Backend**:
   ```powershell
   python main.py
   ```

3. **Install Frontend Dependencies**:
   (Open a new terminal)
   ```powershell
   cd frontend
   npm install
   ```

4. **Run Frontend**:
   ```powershell
   npm run dev
   ```

5. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Tech Stack
- **Frontend**: React (Hooks, Functional Components), Axios, Lucide-React
- **Backend**: FastAPI (Python), SQLite
- **Styling**: Vanilla CSS (Modern Design System)