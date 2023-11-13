from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import time
import json
from os import mkdir, path
import re

headers = Headers(browser="opera", os="lin", headers=True).generate()

def parse_page(response, page):
    soup = BeautifulSoup(response.text, "lxml")
    product_cards = soup.find_all(class_ = "product-card__name")
    for item in product_cards:
        url = item.get("href")
        yield url

def parse_item(item_url):
    time.sleep(0.5)
    item = {}
    response = requests.get(item_url, headers = headers)
    soup = BeautifulSoup(response.text, "lxml")
    name = soup.find(class_ = "breadcrumbs__list").findChildren("li")[-1].text
    chrt = soup.find(class_ = "product-characteristic product-detail-page__product-characteristic").find_all(class_ = "product-characteristic__item")
    item["Название"] = name.strip().lower()
    item['link'] = item_url
    price = soup.find(class_ = "app-price product-sidebar-price__price")
    item["Цена"] = price.text.strip()
    for c in chrt:
        attr_name = c.find(class_ = "product-characteristic__label-holder").text.strip().lower()
        item[attr_name[:-1] if attr_name.endswith(":") else attr_name] = c.find(class_ = "product-characteristic__value").text.strip().lower()
    return item

def parse_site(configs):
    i = 1
    url = configs["search_url"]
    regex = r"page-\d+"
    book_links = []
    print(url)
    while 1:
        page_url = re.sub(regex, f"page-{i}", url)
        response = requests.get(page_url, headers = headers)
        if(response.status_code != 200): break
        for item in parse_page(response, i):
            book_links.append(configs["base"] + str(item))
        print(f"Page {i} scanned...")
        i += 1
    print("All pages scanned, parsing the links...")
    t = time.gmtime()
    if not(path.exists("./data")): mkdir("./data")
    mkdir(f"./data/books_{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}")
    for i in range(len(book_links)):
        link = book_links[i]
        result = parse_item(link)
        with open(f"data/books_{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}/{result['Название']}", "w", encoding = "utf-8") as f:
            json.dump(result, f, ensure_ascii = False, indent = 4)
        print(f"Link {i + 1} parsed, {len(book_links) - i - 1} more links remaining...")