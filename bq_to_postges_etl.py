import os
import logging
import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine, text
from config import Config
from utils.db_connectors.GoogleConnector.bq_connector import BigQueryConnector
from utils.db_connectors.Postgres.postgres_connector import PostgresConnector


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BigQueryToPostgres:
    def __init__(self):
        self.PROJECT_ID = Config.project_id
        self.DATASET_ID = Config.dwh_schema
        self.TABLE_ID = 'fact_user_panel'
        self.service_account_path = Config.serviceAccountCredentialsFilePath
        self.postgres_conn_str = Config.postgres_url

        # Set environment variable for Google Cloud credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.service_account_path

        # Initialize BigQuery client and connector
        self.bq_client = bigquery.Client()
        self.bq_connector = BigQueryConnector(key_path=self.service_account_path)

        # Initialize PostgreSQL connector
        self.postgres_connector = PostgresConnector(connection_url=self.postgres_conn_str)

    def fetch_data_from_bigquery(self):
        query = f"""
        SELECT *
        FROM `{self.PROJECT_ID}.{self.DATASET_ID}.{self.TABLE_ID}`
        """
        try:
            # Fetch data using BigQueryConnector
            df = self.bq_connector.bigquery_run_query(self.PROJECT_ID, self.DATASET_ID, self.TABLE_ID, query)
            if df is None or df.empty:
                logger.warning("No data fetched from BigQuery.")
            else:
                logger.info(f"Data fetched from BigQuery successfully. Number of rows: {len(df)}")
            return df
        except Exception as e:
            logger.error(f"Failed to fetch data from BigQuery: {e}")
            raise

    def load_data_to_postgres(self, df, table_name):
        if df.empty:
            logger.info("No data to upsert.")
            return

        temp_table_name = f"{table_name}_temp_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        try:
            # Create a temporary table to stage the data
            df.to_sql(temp_table_name, con=self.postgres_connector.engine, if_exists='replace', index=False)

            # Specify the columns you want to update on conflict
            columns = [
                "country",
                "avg_price_10",
                "last_weighted_daily_matches_count_10_played_days",
                "active_days_since_last_purchase",
                "score_perc_50_last_5_days",
                "player_last_seen_time",
                "created_at",
                "updated_at"
            ]

            update_columns = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns])

            # Construct the upsert query
            upsert_query = f"""
            INSERT INTO {table_name} (player_id, {', '.join(columns)})
            SELECT player_id, {', '.join(columns)} FROM {temp_table_name}
            ON CONFLICT (player_id)
            DO UPDATE SET {update_columns}
            """

            # Execute the upsert query
            self.postgres_connector.run(upsert_query)

            # Drop the temporary table after upsert
            self.postgres_connector.run(f"DROP TABLE IF EXISTS {temp_table_name}")

            logger.info(f"Data upserted into PostgreSQL table '{table_name}' successfully.")
        except Exception as e:
            logger.error(f"Failed to upsert data into PostgreSQL: {e}")
            raise

    def run(self, table_name):
        try:
            df = self.fetch_data_from_bigquery()
            self.load_data_to_postgres(df, table_name)
        except Exception as e:
            logger.error(f"Error during the run process: {e}")

# Example usage
if __name__ == "__main__":
    bq_to_pg = BigQueryToPostgres()
    bq_to_pg.run('user_panel')

