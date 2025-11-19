from psycopg2.extras import execute_values
from dotenv import load_dotenv
from typing import List 
import psycopg2
import os

load_dotenv()

def create_table():
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    cursor = conn.cursor()
    cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS raw_roles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        company TEXT,
        link TEXT,
        website TEXT,
        description TEXT
      )
      """
    )
    conn.commit()
    print(f"Table 'raw_roles' created successfully or already exists")
    return True

  except psycopg2.Error as e:
    print(f"Error creating table: {e}")
    return False


def insert_roles(roles):
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      execute_values(
        cursor,
        """
        INSERT INTO raw_roles (
          id,
          title,
          company,
          link,
          website
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
          title = EXCLUDED.title,
          company = EXCLUDED.company,
          link = EXCLUDED.link,
          website = EXCLUDED.website 
        """,
        roles 
      )
    
    conn.commit()
    print(f"Successfully inserted {len(roles)} rows.")
  
  except psycopg2.Error as e:
    conn.rollback()
    print(f"Database error: {e}")


def get_links():
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      cursor.execute("SELECT link, id FROM raw_roles;")
      rows = cursor.fetchall()
      links = [r for r in rows]
      
      return links
  
  except Exception as e:
    print(f"Error {e}")


def insert_descriptions(descriptions):
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      cursor.executemany("""
      UPDATE raw_roles
      SET description = %s
      WHERE id = %s
      """, descriptions)
      conn.commit()
      print(f"Successfully inserted {len(descriptions)} descriptions")

      cursor.close()
      conn.close()
    
  except Exception as e:
    conn.rollback()
    print(f"Error: {e}")


