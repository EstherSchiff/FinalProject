import requests
from bs4 import BeautifulSoup
import re
from database import insert_card


class URLError(Exception):
    pass

# gets html from wikipedia page
def get_html():
    url = 'https://en.wikipedia.org/wiki/Playing_cards_in_Unicode#Emoji'
    try:
        request = requests.get(url)
        request.raise_for_status()
    except requests.HTTPError:
        raise URLError("There was a problem reaching the url.")
    return request.text

# gets just the table html
def get_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('table', class_="wikitable nounderlines Unicode")

# extracts the wanted data from the table and filters out unwanted data
def extract_data(table):
    rows = table.find_all('tr')
    skip = ["Reserved", "TRUMP", "FOOL", "JOKER", "BACK", "KNIGHT"]
    cards_data = []
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
                cards_data.append((unicode, name))
    return cards_data

# inserts the extracted data into the database
def insert_data(cards_data):
    for card in cards_data:
        unicode, name = card
        insert_card(unicode, name)

# uses the above functions to scrape card details from wikipedia
def scrape_cards():
    html = get_html()
    table = get_table(html)
    card_data = extract_data(table)
    insert_data(card_data)
