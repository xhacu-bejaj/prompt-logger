# Use a lightweight official Python image
FROM python:3.10-slim 

# Set environment variables for consistency
ENV PYTHONUNBUFFERED 1
ENV APP_PORT 8000

# Set the working directory inside the container
WORKDIR /app

# 1. Copy and install dependencies first. This layer will cache the pip install.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of the application code
COPY . .

# Expose the port (matches the port Uvicorn listens on)
EXPOSE 8000

# Command to run the application using Uvicorn
# 'main:app' references the 'app' object in 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]