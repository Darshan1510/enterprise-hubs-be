# Enterprise Hubs Backend

This is the backend API for the Enterprise Hubs project. The API is built using FastAPI and serves data to the frontend application.

## Prerequisites

- Python (v3.9 or higher)
- pip (v20 or higher)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Darshan1510/enterprise-hubs-be.git
cd enterprise-hubs-be
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check

- **GET** `/api/healthcheck`
  - **Description**: Check the health status of the API.
  - **Response**: `{ "status": "ok" }`

### Companies

- **GET** `/api/companies`
  - **Description**: Get a list of all companies.
  - **Query Parameters**:
    - `name` (optional): Filter companies by name (case-insensitive).
    - `latitude` (optional): Latitude for radius search.
    - `longitude` (optional): Longitude for radius search.
    - `radius` (optional): Radius in kilometers for location-based search (default is 10.0 km).
  - **Response**: A list of companies.

- **GET** `/api/companies/{company_id}`
  - **Description**: Get details of a specific company by ID.
  - **Path Parameters**:
    - `company_id`: The ID of the company to retrieve.
  - **Response**: Details of the company.

- **GET** `/api/companies/{company_id}/locations`
  - **Description**: Get all locations for a specific company ID.
  - **Path Parameters**:
    - `company_id`: The ID of the company whose locations to retrieve.
  - **Response**: A list of locations for the company.

## Docker

### Build and Run with Docker

1. Build the Docker image:

   ```bash
   docker build -t enterprise-hubs-backend .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8000:80 enterprise-hubs-backend
   ```

The API will be available at `http://localhost:8000`.

## Docker Compose

To run the backend and frontend together using Docker Compose, refer to the Docker Compose setup in the main repository.

### Clone the Repositories

```bash
git clone https://github.com/Darshan1510/enterprise-hubs-fe.git
git clone https://github.com/Darshan1510/enterprise-hubs-be.git
```

### Docker Compose Setup

1. Create a `docker-compose.yml` file in the root directory (outside both repositories):

   ```yaml
   version: '3.8'

   services:
     backend:
       container_name: enterprise-hubs-backend
       build:
         context: ./enterprise-hubs-be
         dockerfile: Dockerfile
       ports:
         - "8000:80"
       environment:
         - PYTHONUNBUFFERED=1

     frontend:
       container_name: enterprise-hubs-frontend
       build:
         context: ./enterprise-hubs-fe
         dockerfile: Dockerfile
       ports:
         - "3000:3000"
       depends_on:
         - backend
   ```

2. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

The backend API will be available at `http://localhost:8000`, and the frontend will be available at `http://localhost:3000`.

## License

[MIT](LICENSE)
