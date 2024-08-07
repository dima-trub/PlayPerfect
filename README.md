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

# Attribute Service API

## Overview
The Attribute Service API is a FastAPI application designed to retrieve player attributes from a PostgreSQL database with caching provided by Redis. The service aims to enhance performance by reducing database load through efficient caching strategies.

## Features
- **FastAPI Framework**: Provides a high-performance, easy-to-use API framework.
- **PostgreSQL Integration**: Retrieves data from a PostgreSQL database.
- **Redis Caching**: Implements caching to improve response times and reduce database load.
- **Logging**: Includes detailed logging for monitoring and debugging.
- **Error Handling**: Robust error handling for graceful failure and meaningful responses.





