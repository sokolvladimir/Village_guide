import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.environ.get('token', None)

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'username': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASS', 'postgres'),
    'database': os.environ.get('POSTGRES_DB', 'village_guide')
}
