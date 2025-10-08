# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI and Gradio ports
EXPOSE 8000
EXPOSE 7860

# Start both FastAPI and Gradio
CMD ["python", "run_both.py"]