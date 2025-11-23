# Prompt Logger and Generative AI API



## Overview

This is a **Python FastAPI microservice** that serves as a standardized, robust interface for various Generative AI models, including **Google Gemini**, **OpenAI**, and a **Mock** provider. It is designed with a focus on **observability** and **data persistence**, ensuring every system event and LLM interaction is logged and stored.

### Key Features

* **Provider Abstraction:** Easily switch between different LLM backends (`mock`, `openai`, `google`) via a single API endpoint, simplifying multi-vendor strategies.
* **Database Persistence (SQLite):**
    * **System Logs:** Stores critical events, errors, and warnings in the `logs` table.
    * **Prompt History:** Stores the full user prompt, LLM response, provider used, and latency in the `prompts_and_responses` table.
* **File Logging:** All application activity is mirrored to a local `service.log` file for real-time monitoring.
* **Containerized:** Includes a `Dockerfile` for easy, consistent, and portable deployment using Docker.

---

## Setup & Local Development

### Prerequisites

You will need the following installed:

* **Python 3.10+**
* **pip** (Python package installer)
* **git**
* **(Recommended) Docker**

### 1. Environment Setup

Clone the repository and create a Python virtual environment to manage dependencies:

```bash
# Clone the repository (if applicable)
# git clone <repository-url>
# cd prompt-logger

# Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows Command Prompt

# # 2. Install Dependencies
Install the required Python packages:

# (Optional) Generate the requirements file from your virtual environment
pip freeze > requirements.txt

# Install dependencies
pip install -r requirements.txt
'''

3. Configuration
Create a file named .env in the root directory to manage your settings and sensitive API keys:
'''

# .env file

# Database path (creates a file if it doesn't exist)
DB_PATH=promptlog.db 

# Log file path
LOG_FILE_PATH=service.log

# API Keys for LLM Providers
# If using 'mock', these are not required
GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# General log level
LOG_LEVEL=INFO
'''

4. Run Locally
The application starts, and the required SQLite database tables are initialized automatically on startup.
'''

uvicorn main:app --reload --host 127.0.0.1 --port 8080

Docker Deployment
Use the provided Dockerfile to create a self-contained image ready for any environment.

1. Build the Image
Run the build command from the root directory:

docker build -t prompt-logger-app:latest .

2. Run the Container
Start the application in detached mode, mapping the host port 8080 to the container's internal port 8000:

docker run -d --rm -p 8080:8000 --name prompt-logger-instance prompt-logger-app:latest
'''
3. Verification
Check the container status and stream the logs for verification:
'''
# Check if the container is running
docker ps

# Stream the container logs
docker logs -f prompt-logger-instance

API Endpoints
The core API is served on port 8080. You can access the auto-generated Swagger/OpenAPI documentation at http://localhost:8080/docs.

| Method | Endpoint | Description | Response Example |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Verifies that the server is running. | `{"status": "ok"}` |


| Method | Endpoint | Description |
| :--- | :--- | :--- | 
| POST | /api/generate | The main endpoint for requesting LLM content |

| Parameter | Type | Description | Example
| :--- | :--- | :--- | :--- |
| user_prompt | string | The query sent to the LLM | """Explain quantum physics simply.""" |


3. Admin: View System Logs
Method,Endpoint,Description
GET,/api/admin/history,Retrieves the most recent system log entries (WARNING level and above) from the logs database table.

Query Parameter,Type,Description
lines,integer (max 10),Number of log entries to retrieve.

4. Admin: View Prompt History
Method,Endpoint,Description
GET,/api/admin/prompts,Retrieves the most recent full prompt and response records from the prompts_and_responses database table.

Query Parameter,Type,Description
lines,integer (max 10),Number of records to retrieve.

Example of a successful prompt log entry: The log includes the full interaction for complete auditability.

{
  "id": 1,
  "user_prompt": "Explain quantum physics simply.",
  "llm_response": "Quantum physics studies the tiny world of atoms and subatomic particles, where rules like position and speed are fuzzy and often described by probability.",
  "provider": "google",
  "latency_ms": 1250.78,
  "timestamp": "2023-11-23 11:43:06"
}
'''
