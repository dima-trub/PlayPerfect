import os

class Config:
    INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data/')
    serviceAccountCredentialsFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'playperfect-431512-cb9ed2e92223.json')
    project_id = 'playperfect-431512'
    stg_schema = 'stg'
    dwh_schema = 'dwh'
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    postgres_url = os.getenv('POSTGRES_URL', 'postgresql://postgres:postgres@localhost:5432/mydatabase')
