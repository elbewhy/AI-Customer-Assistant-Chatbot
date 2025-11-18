#!/usr/bin/env bash
set -e

# --- 1. Install Node dependencies (for Tailwind) ---
# Node is needed to compile the CSS. Render automatically provides Node/npm.
echo "Installing Node Dependencies (Tailwind)..."
npm install

# --- 2. Compile Tailwind CSS (This fixes the recurring UI issue) ---
echo "Compiling Tailwind CSS and Custom Styles..."
# This command reads your input.css (which MUST contain the @tailwind directives)
# and creates the final output.css file that your HTML links to.
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

# --- 3. Install Python dependencies ---
echo "Installing Python Requirements..."
pip install -r requirements.txt

# --- 4. Start the Flask server ---
# This is the final step that keeps the web service running.
echo "Starting Gunicorn Server..."
# Using exec ensures Gunicorn takes over the PID of the script
exec gunicorn app:app
