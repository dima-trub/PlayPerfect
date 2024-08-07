# FastAPI Project with BigQuery and PostgreSQL

This project is a FastAPI-based application that integrates with Google BigQuery and PostgreSQL. It provides endpoints to query player attributes and includes an ETL pipeline to transfer data between BigQuery and PostgreSQL.

## Overview

- **FastAPI Application**: Offers an API endpoint to retrieve player attributes. It uses Redis for caching to improve performance.
- **ETL Pipeline**: Manages the ETL (Extract, Transform, Load) process from Google BigQuery to PostgreSQL. It fetches data from a BigQuery table and upserts it into a PostgreSQL table.
- **Configuration Management**: Handles environment-specific settings and credentials.
- **Docker Support**: Provides a `docker-compose` setup to manage the application, Redis, and PostgreSQL services.
- **Testing Script**: Includes a script to test the API endpoint and trigger the ETL process.

## Files

### `api_pipeline.py`

Handles the FastAPI application that provides an endpoint to fetch player attributes. It uses Redis for caching to improve performance.

### `bq_to_postges_etl.py`

This script handles the ETL process from Google BigQuery to PostgreSQL. It fetches data from a specified BigQuery table and loads it into a PostgreSQL table using an upsert strategy to handle existing records.

### `config.py`

Contains configuration settings for the project, including paths to credentials and connection URLs.

### `docker-compose.yml`

Defines the Docker services for the FastAPI application, Redis, and PostgreSQL. It sets up the environment and dependencies for running the project in Docker containers.

### `Dockerfile`

Specifies how to build the Docker image for the FastAPI application, including setting up the environment and installing dependencies.

### `requirements.txt`

Lists the Python packages required for the project.

### `requests_test.py`

A script for testing the FastAPI endpoint and triggering the ETL process.

## Installation

### Clone the Repository

Project Setup and Installation
This README provides instructions for setting up and running the project, including both local and Docker-based setups.
Install Dependencies
Create a virtual environment (optional but recommended) and install the required packages:
bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

Docker Setup
If you prefer using Docker, ensure Docker and Docker Compose are installed on your machine.
To build and run the Docker containers:
bash
docker-compose up --build

This command starts the FastAPI application, Redis, and PostgreSQL services.
Running the Application
With Docker
The FastAPI application will be available at http://127.0.0.1:8000.
Without Docker
Run the FastAPI application directly:
bash
python api_pipeline.py

Running Tests
To test the FastAPI endpoint and run the ETL pipeline:
bash
python requests_test.py

This script sends a request to the FastAPI endpoint and, based on the response, triggers the api_pipeline.py script.
Configuration
Update the config.py file with the appropriate paths and credentials:
Google Cloud Service Account Key Path
Project ID
BigQuery Dataset and Table
PostgreSQL Connection URL
Redis Connection URL
Notes
Ensure that environment variables for REDIS_URL and POSTGRES_URL are set correctly if you are running the services outside Docker.
The requirements.txt file lists all the dependencies needed for the project.

```bash
git clone https://github.com/dima-trub/PlayPerfect.git
cd PlayPerfect

