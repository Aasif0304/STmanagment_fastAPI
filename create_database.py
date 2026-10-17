
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_USER = "postgres"
DB_PASSWORD = "Mohamedaasif1"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "student_management_fastapi"

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    cursor.execute(
        f'CREATE DATABASE "{DB_NAME}"'
    )

    print(f"Database '{DB_NAME}' created successfully!")

    cursor.close()
    connection.close()

except psycopg2.errors.DuplicateDatabase:
    print(f"Database '{DB_NAME}' already exists!")

except Exception as error:
    print("Database creation failed:", error)
