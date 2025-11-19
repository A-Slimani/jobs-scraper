from database import create_table, insert_roles
from download import get_webpage_content
from lxml import html
import requests
import os

def extract_roles(filepath):
  try:
    roles = {} 

    tree = html.parse(filepath)
    root = tree.getroot()

    role_cards = root.xpath("//article[@data-automation='normalJob']")

    for card in role_cards:
      url_part = card.xpath("*//a[@data-automation='jobTitle']")[0].get('href')

      id = int(url_part.split('?')[0].split('/')[-1])
      title = card.xpath("*//a[@data-automation='jobTitle']")[0].text.strip()

      company_elements = card.xpath("*//a[@data-automation='jobCompany']")
      company = company_elements[0].text.strip() if company_elements else None

      link = f"https://www.seek.com{url_part}"
      website = "seek"

      roles[id] = (id, title, company, link, website)

    return roles
  
  except IndexError:
    print(f"Error for role {id, title} index out of range")

  except Exception as e:
    print(f"Error: {e}")
    pass


def extract_description(filepath):
  tree = html.parse(filepath)
  root = tree.getroot()

  description_element = root.xpath("*//div[@data-automation='jobAdDetails']")[0]

  description_nodes = description_element.xpath('./descendant::text()')
  description = "" 
  for d in description_nodes:
    description += d
    
  return description