from sqlalchemy import create_engine, text
from typing import Dict, Optional
import logging
import pandas as pd
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresConnector:
    def __init__(self, connection_url: str):
        self.engine = create_engine(connection_url)
        logger.info(f"PostgresConnector initialized with URL: {connection_url}")

    def run(self, query: str, parameters: Optional[Dict] = None):
        with self.engine.connect() as conn:
            with conn.begin():
                try:
                    logger.info(f"Executing query: {query}")
                    conn.execute(text(query), parameters)
                    logger.info("Query executed successfully.")
                except Exception as e:
                    logger.error(f"Error executing query: {e}")
                    conn.rollback()
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

    def test_query(self):
        query = "SELECT * FROM user_panel"
        try:
            result = self.select(query)
            if result is not None and not result.empty:
                logger.info("Query result:")
                logger.info(result.head())
            else:
                logger.info("No data found or result is empty.")
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    postgres_connector = PostgresConnector(connection_url=Config.postgres_url)
    postgres_connector.test_query()
