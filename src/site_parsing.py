from bs4 import BeautifulSoup
from requests import get
from fake_headers import Headers
import re
from .logging import no_log


headers = Headers(browser="opera", os="lin", headers=True).generate()


def parse_page(response) -> str:
    """
    Parse the page, extract the product card links

    Yields None if the html document is not correct
    """

    soup = BeautifulSoup(response.text, "lxml")
    product_cards = soup.find_all(class_ = "product-card__name")
    for item in product_cards:
        try:
            url = item.get("href")
            yield url
        except:
            yield None


def parse_item(item_url: str) -> dict:
    """
    Parse the product card page, return dictionary with product's characteristics

    Returns None if the page is not correct
    """

    try:
        response = get(item_url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find(class_ = "breadcrumbs__list").findChildren("li")[-1].text
        
        price = soup.find(class_ = "app-price product-sidebar-price__price")
        if (price == None): price = "Нет в наличии" 
        else: price = price.text.strip()
        item = {"Название": name.strip().lower(), "Ссылка": item_url, "Цена": price}

        # All other product's characteristics
        chrt = soup.find(class_ = "product-characteristic product-detail-page__product-characteristic").find_all(class_ = "product-characteristic__item")
        for c in chrt:
            attr_name = c.find(class_ = "product-characteristic__label-holder").text.strip().lower()
            item[attr_name[:-1] if attr_name.endswith(":") else attr_name] = c.find(class_ = "product-characteristic__value").text.strip().lower()
        return item
    except Exception:
        return None


def parse_site(configs: dict, logging: callable = no_log) -> None:
    """
    Parse the page from configs
    """

    url = configs["search_url"]
    regex = r"page-\d+"
    book_links = []
    i = 1
    while True:
        page_url = re.sub(regex, f"page-{i}", url)
        response = get(page_url, headers = headers)

        # In case there are no more pages
        if(response.status_code != 200): break

        for item in parse_page(response):
            if (item == None):
                logging("[INFO] Encountered invalid page")
            book_links.append(configs["base"] + str(item))

        logging(f"[INFO] Page {i} scanned...")
        i += 1
    logging("[INFO] All pages scanned, parsing the links...")

    for i in range(len(book_links)):
        link = book_links[i]
        result = parse_item(link)
        if (result == None):
            logging(f"[INFO] Link {i + 1} leads to incorrect page")
            continue
        logging(f"[INFO] Link {i + 1} parsed, {len(book_links) - i - 1} more links remaining...")
        yield result