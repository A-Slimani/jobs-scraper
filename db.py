from psycopg2.extras import execute_values
import psycopg2
import os

def create_table():
  conn = psycopg2.connect(os.getenv("DB_URI"))
  cursor = conn.cursor()
  cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS raw_roles
      id INTEGER PRIMARY KEY,
      title TEXT,
      company TEXT,
      link TEXT,
      role_description TEXT
    """
  )

def insert_roles(roles):
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      execute_values(
        cursor,
        """
        INSERT INTO raw_roles
        (
          id,
          title,
          company,
          link
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
          title = EXCLUDED.title,
          company = EXCLUDED.company,
          link = EXCLUDED.link
        """,
        roles 
      )
    
    conn.commit()
    print(f"Successfully inserted {len(roles)} rows.")
  
  except psycopg2.Error as e:
    conn.rollback()
    print(f"Database error: {e}")
