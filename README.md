FastAPI Project with BigQuery and PostgreSQL
This project is a FastAPI-based application that integrates with Google BigQuery and PostgreSQL. It provides endpoints to query player attributes and includes an ETL pipeline to transfer data between BigQuery and PostgreSQL.

Overview
FastAPI Application: Offers an API endpoint to retrieve player attributes. It caches results in Redis to optimize performance.
ETL Pipeline: Transfers data from BigQuery to PostgreSQL. This includes fetching data from a BigQuery table and upserting it into a PostgreSQL table.
Configuration Management: Handles environment-specific settings and credentials.
Docker Support: Provides a docker-compose setup to manage the application, Redis, and PostgreSQL services.
Testing Script: Includes a script to test the API endpoint and trigger the ETL process.
bq_to_postges_etl.py
This script handles the ETL (Extract, Transform, Load) process from Google BigQuery to PostgreSQL. It fetches data from a specified BigQuery table and loads it into a PostgreSQL table, using an upsert strategy to handle existing records.

Fetch Data: Retrieves data from a BigQuery table and returns it as a pandas DataFrame.
Load Data: Stages the data into a temporary table in PostgreSQL, performs an upsert operation, and then cleans up the temporary table.
Installation
Clone the Repository
bash
Copy code
git clone https://github.com/dima-trub/PlayPerfect.git
cd PlayPerfect
Install Dependencies
Create a virtual environment (optional but recommended) and install the required packages:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Docker Setup
If you prefer using Docker, ensure Docker and Docker Compose are installed on your machine.

To build and run the Docker containers:

bash
Copy code
docker-compose up --build
This command starts the FastAPI application, Redis, and PostgreSQL services.

Running the Application
With Docker
The FastAPI application will be available at http://127.0.0.1:8000.

Without Docker
Run the FastAPI application directly:

bash
Copy code
python api_pipeline.py
Running Tests
To test the FastAPI endpoint and run the ETL pipeline:

bash
Copy code
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
