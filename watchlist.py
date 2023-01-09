import gzip
import json
import os
import shutil
from bs4 import BeautifulSoup
import requests
import re
BASE_URL = "https://www.opendoorsus.org/en-US"


COUNTRY_URLS = []
OUT = {}

# get country urls
p = requests.get(f"{BASE_URL}/persecution/countries/")

# with open("data/index.html", "w") as outfile:
#     outfile.write(p.text)

soup = BeautifulSoup(p.text, "html.parser")
links = soup.find_all('a', class_="view-more", href=True)

# print(links)

# get meta from main page.. half is there and half in the details. not
# much overlap.

countries = soup.find_all('a', attrs={'xlink:href':"#"})
for country in countries:
    data = country.find('path')

    v_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"Violence\"\]\s*?=\s*?(.+?);",p.text, re.I)
    v = v_re.group(1) if v_re else ""

    cl_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"Church Life\"\]\s*?=\s*?(.+?);",p.text, re.I)
    cl = cl_re.group(1) if cl_re else ""

    nl_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"National Life\"\]\s*?=\s*?(.+?);",p.text, re.I)
    nl = nl_re.group(1) if nl_re else ""

    coml_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"Community Life\"\]\s*?=\s*?(.+?);",p.text, re.I)
    coml = coml_re.group(1) if coml_re else ""

    fl_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"Family Life\"\]\s*?=\s*?(.+?);",p.text, re.I)
    fl = fl_re.group(1) if fl_re else ""

    pl_re = re.search(rf"mapData\[2022\]\[\"{data.get('data-name')}\"\]\[\"Private Life\"\]\s*?=\s*?(.+?);",p.text, re.I)
    pl = pl_re.group(1) if pl_re else ""

    OUT[data.get('data-name')] = {
      "name": data.get('data-name').strip(),
      "rank": data.get('data-rank').strip(),
      "religion": data.get('data-religion').strip(),
      "government": data.get("data-government").strip(),
      "christians": data.get('data-christians').strip(),
      "violence":v,
      "church_life": cl,
      "national_life":nl,
      "community_life":coml,
      "family_life":fl,
      "private_life":pl,
    }


# print(links)

# iterate countries and get the region
for country in links:
    print(country.get('href'))
    d = requests.get(f"{BASE_URL}{country.get('href')}")

    soup = BeautifulSoup(d.text, "html.parser")

    if not soup.find("h6",text="Main Religion"):
        print("skipping")
        continue

    OUT[soup.find("h1").text.strip()]["persecution_type"] =  soup.find("h6",text=re.compile(r'Persecution Type|Main threat')).find_next_sibling().text.strip()
    OUT[soup.find("h1").text.strip()]["details"] = soup.find("div",class_="wwl-country__body").text.strip()
    OUT[soup.find("h1").text.strip()]["url"] = BASE_URL+country.get('href')
    
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

