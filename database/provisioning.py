import psycopg2
from psycopg2 import sql

ADMIN_DB_URL = "postgresql://postgres:haggag@localhost:5432/postgres"

def create_tenant_db(tenant_name: str):
    conn = psycopg2.connect(ADMIN_DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # 1. check if exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (tenant_name,))
    exists = cur.fetchone()

    if exists:
        print(f"DB already exists: {tenant_name}")
        return

    # 2. create database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(tenant_name)
    ))

    print(f"Database created: {tenant_name}")

    cur.close()
    conn.close()