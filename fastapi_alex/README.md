# TODO Service and URL Shortener

This repository contains two services:
1. **TODO Service**: A task management API.
2. **URL Shortener**: A URL shortening service.

## How to Run the Services

### Running Locally

#### Prerequisites:
- Python 3.8 or higher
- `pip` for dependency management

#### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/MasterHach/WEB_BASIS_TECH.git
   cd fastapi_alex
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize necessary directories for SQLite data:
   ```bash
   mkdir -p data
   ```

4. Run the services:
   - For TODO Service:
     ```bash
     uvicorn todo_app.main:app --host 0.0.0.0 --port 8080
     ```
   - For URL Shortener:
     ```bash
     uvicorn url_shortener.main:app --host 0.0.0.0 --port 8000
     ```

5. Access the services:
   - TODO Service Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
   - URL Shortener Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Running with Docker

#### Prerequisites:
- Docker installed and running

#### Steps:
1. Build the Docker images:
   - For TODO Service:
     ```bash
     docker build -t todo-service -f todo_app/Dockerfile .
     ```
   - For URL Shortener:
     ```bash
     docker build -t url-shortener -f url_shortener/Dockerfile .
     ```

2. Run the containers:
   - For TODO Service:
     ```bash
     docker run -d -p 8080:8080 -v todo_data:/app/data todo-service
     ```
   - For URL Shortener:
     ```bash
     docker run -d -p 8000:8000 -v shortener_data:/app/data url-shortener
     ```

3. Access the services:
   - TODO Service Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
   - URL Shortener Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Features

#### TODO Service:
- Create, update, delete, and list tasks
- Search tasks by title or description
- Mark tasks as complete

#### URL Shortener:
- Create short URLs
- Redirect to original URLs
- View statistics (click count)
- List top clicked URLs