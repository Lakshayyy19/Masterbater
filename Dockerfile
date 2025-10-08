# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for OpenCV & Ultralytics)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI and Gradio ports
EXPOSE 8000
EXPOSE 7860

# Start both FastAPI and Gradio
CMD ["python", "run_both.py"]