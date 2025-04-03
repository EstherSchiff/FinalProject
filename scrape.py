import requests
from bs4 import BeautifulSoup
import re
from database import insert_card


def scrape_cards():
    # URL for scrapping data
    url = 'https://en.wikipedia.org/wiki/Playing_cards_in_Unicode#Emoji'

    # get URL html
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table', class_="wikitable nounderlines Unicode")
    rows = table.find_all('tr')
    skip = ["Reserved", "TRUMP", "FOOL", "JOKER", "BACK", "KNIGHT"]

    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            title = cell.get('title', "")
            if title and not any(sub in title for sub in skip):
                unicode_match = re.search(r"U\+1F0[A-D][0-9A-F]", title)
                unicode = unicode_match.group(0)
                name_match = re.search(
                    r"(PLAYING CARD\s+)([A-Za-z0-9\s]+)", title)
                name = name_match.group(2)
                insert_card(unicode, name)
