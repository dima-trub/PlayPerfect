# FastAPI Project with BigQuery and PostgreSQL

This project is a FastAPI-based application that integrates with Google BigQuery and PostgreSQL. It provides endpoints to query player attributes and includes an ETL pipeline to transfer data between BigQuery and PostgreSQL.

## Overview

- **FastAPI Application:** Offers an API endpoint to retrieve player attributes. It caches results in Redis to optimize performance.
- **ETL Pipeline:** Transfers data from BigQuery to PostgreSQL. This includes fetching data from a BigQuery table and upserting it into a PostgreSQL table.
- **Configuration Management:** Handles environment-specific settings and credentials.
- **Docker Support:** Provides a docker-compose setup to manage the application, Redis, and PostgreSQL services.
- **Testing Script:** Includes a script to test the API endpoint and trigger the ETL process.

## bq_to_postges_etl.py

This script handles the ETL (Extract, Transform, Load) process from Google BigQuery to PostgreSQL. It fetches data from a specified BigQuery table and loads it into a PostgreSQL table, using an upsert strategy to handle existing records.

- **Fetch Data:** Retrieves data from a BigQuery table and returns it as a pandas DataFrame.
- **Load Data:** Stages the data into a temporary table in PostgreSQL, performs an upsert operation, and then cleans up the temporary table.

## Installation

### Clone the Repository

```bash
git clone https://github.com/dima-trub/PlayPerfect.git
cd PlayPerfect


## Install Dependencies

Create a virtual environment (optional but recommended) and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

## Docker Setup

If you prefer using Docker, make sure Docker and Docker Compose are installed on your machine.

### Build and Run Docker Containers

To build and start the Docker containers, run the following command:

```bash
docker-compose up --build
