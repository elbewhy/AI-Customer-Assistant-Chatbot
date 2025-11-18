# Base image (might be Python or another image)
# ... your existing Dockerfile lines ...

# 1. Install Node/npm and Python
# (Ensure your base image supports both, or install them here if needed)

# 2. Install Node dependencies (for Tailwind)
COPY package.json package-lock.json ./
RUN npm install

# 3. Compile Tailwind CSS
# This creates static/css/output.css
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

# 4. Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ... rest of your Dockerfile (COPY app files, ENTRYPOINT, etc.)

# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Create virtualenv and install deps
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port and run gunicorn
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2"]
