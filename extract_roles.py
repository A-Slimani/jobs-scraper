from db import create_table, insert_roles
from lxml import html
import os

def extract_roles(filepath):
  try:
    roles = []

    tree = html.parse(filepath)
    root = tree.getroot()

    role_cards = root.xpath("//article[@data-automation='normalJob']")

    for card in role_cards:
      url_part = card.xpath("*//a[@data-automation='jobTitle']")[0].get('href')

      id = url_part.split('?')[0]
      title = card.xpath("*//a[@data-automation='jobTitle']")[0].text.strip()
      company = card.xpath("*//a[@data-automation='jobCompany']")[0].text.strip()
      link = f"https://www.seek.com{url_part}"
      website = "seek"

      roles.append({
        "id": id,
        "title": title,
        "company": company,
        "link": link,
        "website": website
      })

    return roles

  except Exception as e:
    print(f"Error: {e}")
    pass


if __name__ == "__main__":
  path = "./seek_roles"
  file_names = [f"{path}/{fn}" for fn in os.listdir(path)]

  for fn in file_names:
    roles = extract_roles(fn)  