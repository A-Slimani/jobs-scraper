from psycopg2.extras import execute_values
from dotenv import load_dotenv
import psycopg2
from random import randint
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

def get_random_description():
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      cursor.execute("""
      SELECT description
      FROM raw_roles
      WHERE description IS NOT NULL
      ORDER BY RANDOM()
      LIMIT 1
      """)
      row = cursor.fetchone()[0]

      cursor.close()
      conn.close()

      return row
  
  except Exception as e:
    print(f"Error fetching random role description: {e}")
    cursor.close()
    conn.close()


def get_all_descriptions():
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    with conn.cursor() as cursor:
      cursor.execute("""
      SELECT description 
      FROM raw_roles
      WHERE description IS NOT NULL
      LIMIT 10
      """)
      row = cursor.fetchall()

      descriptions = [d[0] for d in row]

      cursor.close()
      conn.close()

      return descriptions
  
  except Exception as e:
    print(f"Error fetching all descriptions: {e}")
    cursor.close()
    conn.close()
