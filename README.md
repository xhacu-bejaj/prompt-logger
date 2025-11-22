Prompt Logger and Generative AI API

Overview

This is a Python FastAPI microservice designed to serve as a standardized interface for various Generative AI models (Mock, Google Gemini, OpenAI). The application provides robust logging and persistence features, saving system events (logs) and prompt/response data into a local SQLite database and a file.

Key Features

Provider Abstraction: Easily switch between LLM providers (Mock, OpenAI, Google) via a single API endpoint.

Database Persistence: Uses SQLite to store:

System Logs: Critical events, errors, and warnings (logs table).

Prompt History: The full user prompt, LLM response, provider, and latency (prompts_and_responses table).

File Logging: All application activity is mirrored to a service.log file.

Containerized: Includes a Dockerfile for easy, consistent deployment via Docker.

Setup & Local Development

Prerequisites

Python 3.10+

pip (Python package installer)

git

(Optional, but highly recommended) Docker

1. Environment Setup

Clone the repository and set up your virtual environment:

# Clone the repository (if applicable)
# git clone <repository-url>
# cd prompt-logger

# Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows Command Prompt


2. Install Dependencies

Ensure your requirements.txt is up to date, then install:

# Generate the requirements file from your virtual environment
pip freeze > requirements.txt

# Install dependencies
pip install -r requirements.txt


3. Configuration

Create a .env file in the root directory to manage settings and API keys.

# .env file
# Database path (creates a file if it doesn't exist)
DB_PATH=promptlog.db 

# Log file path
LOG_FILE_PATH=service.log

# API Keys for LLM Providers
# If using 'mock', these are not required
GOOGLE_API_KEY=""
OPENAI_API_KEY=""

# General log level
LOG_LEVEL=INFO


4. Run Locally

The application starts with database tables automatically initialized.

uvicorn main:app --reload --host 127.0.0.1 --port 8080


The application will be accessible at http://127.0.0.1:8080.

Docker Deployment

The provided Dockerfile creates an efficient, self-contained image ready for any environment.

1. Build the Image

Run the build command from the root directory:

docker build -t prompt-logger-app:latest .


2. Run the Container

Start the application in a detached mode, mapping the host port 8080 to the container port 8000.

docker run -d --rm -p 8080:8000 --name prompt-logger-instance prompt-logger-app:latest


3. Verification

Check the container status and logs:

# Check if the container is running
docker ps

# Stream the container logs
docker logs -f prompt-logger-instance


API Endpoints

The core API runs on port 8080 (or your configured port). You can access the auto-generated documentation at http://localhost:8080/docs.

1. Health Check

GET /api/health
Verifies that the server is running.

Response: {"status": "ok"}

2. Generate Content

POST /api/generate
The main endpoint for requesting LLM content.

Parameter

Type

Description

Example

user_prompt

string

The query sent to the LLM.

"Explain quantum physics simply."

provider

string

The LLM backend to use.

"mock" (or "openai", "google")

3. Admin: View System Logs

GET /api/admin/history
Retrieves the most recent system log entries (WARNING level and above) from the logs database table.

Query Parameter: lines (integer, max 10) - Number of entries to retrieve.

4. Admin: View Prompt History

GET /api/admin/prompts
Retrieves the most recent full prompt and response records from the prompts_and_responses database table.

Query Parameter: lines (integer, max 10) - Number of entries to retrieve.

Example of a successful prompt log entry accessed via /api/admin/prompts.
