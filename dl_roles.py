from datetime import date
from pathlib import Path 
import requests

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:145.0) Gecko/20100101 Firefox/145.0'
}

def get_webpage_content(url):
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    return html_content
  
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return None


def save_content(dir, filename, content):
  dir_path = Path(dir)

  if not dir_path.is_dir():
    dir_path.mkdir(exist_ok=True)

  try:
    with open(f"{dir}/{filename}", 'w', encoding='utf-8') as f:
      f.write(content)
    
    return True
  
  except Exception as e:
    print("failed to write: ", e)
        

if __name__ == "__main__":
  seek_url = "https://www.seek.com.au/data-engineer-jobs/in-All-Sydney-NSW"
  for i in range(1, 30):
    dir = "./seek_roles"
    filename = f"{date.today()}-seek_roles_page-{i}.html" 
    content = get_webpage_content(f"{seek_url}?page={i}")    
    save_content(dir, filename, content)