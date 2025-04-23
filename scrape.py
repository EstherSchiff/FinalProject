from scrape_helpers import get_html, get_table, extract_data, insert_data

# scrape card details from wikipedia
def scrape_cards():
    html = get_html()
    table = get_table(html)
    card_data = extract_data(table)
    insert_data(card_data)
