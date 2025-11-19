from db import create_table, insert_roles, insert_descriptions, get_links
from extract_roles import extract_roles, extract_description
from dl_roles import get_webpage_content, save_content
from datetime import date
from pathlib import Path
import argparse
import os

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Seek Scraper')
  parser.add_argument('-a', '--all', action='store_true', help='run full stack')
  parser.add_argument('--download-roles', action='store_true', help='download pages')
  parser.add_argument('--extract-roles', action='store_true', help='extract and upload roles to db')
  parser.add_argument('--download-description', action='store_true', help='download each role page')
  parser.add_argument('--extract-description', action='store_true', help='extract descriptions from roles')


  # dl web pages
  args = parser.parse_args()
  if args.download_roles:
    dir = "./seek_roles"
    seek_url = "https://www.seek.com.au/data-engineer-jobs/in-All-Sydney-NSW"
    for i in range(1, 30):
      file_name = f"{date.today()}-seek_roles_page-{i}.html" 
      file_path = Path(f"{dir}/{file_name}") 

      if not file_path.exists():
        content = get_webpage_content(f"{seek_url}?page={i}")    
        save_content(dir, file_name, content)
      else:
        print(f"{file_name} already exists")

  # extract and upload roles 
  if args.extract_roles:
    create_table()  

    path = "./seek_roles"
    file_names = [f"{path}/{fn}" for fn in os.listdir(path)]

    r_list = [extract_roles(fn) for fn in file_names]
    r_merged = {}

    for d in r_list:
      r_merged.update(d)

    insert_roles(r_merged.values())

  # # extract and upload description
  if args.download_description:
    try: 
      dir = './seek_roles/descriptions/'
      for link in get_links():
        file_name = f"{link[1]}-{date.today()}-description.html"
        file_path = Path(f"{dir}/{file_name}") 

        if not file_path.exists():
          content = get_webpage_content(link[0])
          save_content(dir, file_name, content)
        else:
          print(f"{file_name} already exists")
    
    except Exception as e:
      print(f"download error: {e}")
  
  if args.extract_description:
    try:
      path = "./seek_roles/descriptions"
      file_names = [f"{path}/{fn}" for fn in os.listdir(path)]
      descriptions = []
      for f in file_names: 
        id = f.split('-')[0].split('/')[-1]
        d = extract_description(f)
        descriptions.append((d, id))

      insert_descriptions(descriptions)
    
    except Exception as e:
      print(f"Extraction error: {e}")

     