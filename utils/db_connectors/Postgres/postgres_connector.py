from sqlalchemy import create_engine, text
from typing import Dict, Optional, Tuple, Any
import logging
import pandas as pd
import psycopg2
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresConnector:
    def __init__(self, connection_url: str):
        self.engine = create_engine(connection_url)
        self.conn = None
        self.cursor = None
        logger.info(f"PostgresConnector initialized with URL: {connection_url}")

    def run(self, query: str, parameters: Optional[Dict] = None):
        with self.engine.connect() as conn:
            try:
                logger.info(f"Executing query: {query}")
                conn.execute(text(query), parameters)
                logger.info("Query executed successfully.")
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                raise

    def select(self, query: str) -> pd.DataFrame:
        with self.engine.connect() as conn:
            try:
                logger.info(f"Executing query: {query}")
                result = conn.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()
                df = pd.DataFrame(rows, columns=columns)
                logger.info("Query results loaded into DataFrame successfully.")
                return df
            except Exception as e:
                logger.error(f"Error while running query: {e}")
                raise

    # def test_query(self):
    #     query = "SELECT * FROM user_panel LIMIT 5"  # Added LIMIT for testing
    #     try:
    #         result = self.select(query)
    #         if not result.empty:
    #             logger.info("Query result:")
    #             logger.info(result.head())
    #         else:
    #             logger.info("No data found or result is empty.")
    #     except Exception as e:
    #         logger.error(f"Error: {e}")

    def connect_psycopg2(self):
        try:
            self.conn = psycopg2.connect(Config.postgres_url)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            logger.info("Psycopg2 connection and cursor initialized.")
        except Exception as e:
            logger.error(f"Error connecting with psycopg2: {e}")
            raise

    def close_psycopg2(self):
        try:
            if self.cursor:
                self.cursor.close()
                logger.info("Psycopg2 cursor closed.")
            if self.conn:
                self.conn.close()
                logger.info("Psycopg2 connection closed.")
        except Exception as e:
            logger.error(f"Error closing psycopg2 connection: {e}")
            raise

    def execute_and_fetchone(self, query: str, params: Tuple[Any, ...]) -> Optional[Tuple[Any, ...]]:
        if not self.cursor:
            raise RuntimeError("Psycopg2 connection not initialized.")
        try:
            logger.info(f"Executing query: {query} with params: {params}")
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            logger.info("Query executed and result fetched successfully.")
            return result
        except Exception as e:
            logger.error(f"Error executing query with psycopg2: {e}")
            raise

# if __name__ == "__main__":
#     postgres_connector = PostgresConnector(connection_url=Config.postgres_url)
#     postgres_connector.test_query()
#
#     # Example usage of psycopg2 connection
#     postgres_connector.connect_psycopg2()
#     player_id = '6671adc3dd588a8bda049551' # Example parameter
#     query = "SELECT * FROM user_panel WHERE player_id = %s"
#     result = postgres_connector.execute_and_fetchone(query, (player_id,))
#     logger.info(f"Fetched result: {result}")
#     postgres_connector.close_psycopg2()