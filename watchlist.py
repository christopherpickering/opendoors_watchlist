import gzip
import json
import os
import shutil
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.opendoorsusa.org/christian-persecution/world-watch-list/"


COUNTRY_URLS = []
OUT = {}

# get country urls
p = requests.get(f"{BASE_URL}")

soup = BeautifulSoup(p.text, "html.parser")
links = soup.find_all('a', class_="country-item", href=True)

# print(links)
# page_json = p.json()

# results = page_json["result"]["data"]["countries"]["edges"]

# # iterate countries and get the region
for country in links:

    d = requests.get(country.get('href'))

    soup = BeautifulSoup(d.text, "html.parser")


    OUT[country.get("data-country")] = {
      "name": country.get("data-country"),
      "rank": country.get("data-rank"),
      "region": soup.find("span",text="Region").find_next_sibling().text.strip(),
      "religion": soup.find("span",text="Religion").find_next_sibling().text.strip(),
      "score": soup.find("span",text="Score").find_next_sibling().text.strip(),
      "persecution_type": soup.find("span",text="Persecution Type").find_next_sibling().text.strip(),
      "violence":soup.find("td",text="Violence").find_next_sibling().text.strip(),
      "church_life":soup.find("td",text="Church Life").find_next_sibling().text.strip(),
      "national_life":soup.find("td",text="National Life").find_next_sibling().text.strip(),
      "community_life":soup.find("td",text="Community Life").find_next_sibling().text.strip(),
      "family_life":soup.find("td",text="Family Life").find_next_sibling().text.strip(),
      "private_life":soup.find("td",text="Private Life").find_next_sibling().text.strip(),
      "details":soup.find("div",class_="about-content").text.strip(),
      "url": country.get('href')
    }
    # break

if not os.path.isdir("data"):
    os.makedirs("data")

json_object = json.dumps(OUT, indent=4)
with open("data/opendoors_watchlist.json", "w") as outfile:
    outfile.write(json_object)

# gzip version
with open("data/opendoors_watchlist.json", "rb") as infile:
    with gzip.open("data/opendoors_watchlist.json.gz", "wb") as outfile:
        shutil.copyfileobj(infile, outfile)

