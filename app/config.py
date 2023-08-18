import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.environ.get('token', None)

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': os.environ.get('POSTGRES_PORT', '5432'),
    'username': os.environ.get('POSTGRES_USER', 'postgres'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    'database': os.environ.get('POSTGRES_NAME', 'village_guide')
}
