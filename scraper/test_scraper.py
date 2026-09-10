import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and makes its values available

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

print("Connected successfully!")
conn.close()