import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

class PostgresRetriever:
    def __init__(self, db_url: str = None):
        load_dotenv(override=True)
        self.db_url = db_url or os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/finance_db")

    def execute_query(self, sql_query: str) -> list[dict]:
        """Executes a dynamic SQL query and returns records as a dictionary."""
        conn = None
        try:
            conn = psycopg2.connect(self.db_url)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql_query)
                records = cursor.fetchall()
                return [dict(row) for row in records]
        except Exception as e:
            return [{"error": f"Database execution failed: {str(e)}"}]
        finally:
            if conn:
                conn.close()